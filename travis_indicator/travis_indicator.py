#!/usr/bin/env python3

import datetime
import pprint
import travispy
import signal
import time
import os
import gi
import threading
import configparser
import webbrowser
import timeago
import pytz
import dateutil.parser

import sys

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from gi.repository import GLib as glib
from gi.repository import GObject as gobject
from gi.repository import GdkPixbuf as gdkpixbuf

APPINDICATOR_ID = 'travis_indicator'

class Indicator:
  def __init__(self, auth_token, update_rate, github_user=None):
    self._init_indicator()
    self._init_icons()
    self.update_rate = int(update_rate) # in seconds
    self.github_user = github_user
    self._init_travis(auth_token)
    self._update_status()
    
    # the thread:
    self.update = threading.Thread(target=self.update)
    
    # daemonize the thread to make the indicator stopable
    self.update.setDaemon(True)
    self.update.start()
    
    
  def _init_indicator(self):
    # init indicator
    self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('logo.svg'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    self.app = APPINDICATOR_ID
    
    # init notify
    notify.init(APPINDICATOR_ID)
  
  
  def _init_icons(self):
    # prepare icons
    self.iconsizes = gtk.IconSize.lookup(gtk.IconSize.MENU)
    
    # mapping from state to available state icons (job_*.svg)
    self.state_icon = dict()
    self.state_icon['canceled'] = 'canceled'
    self.state_icon['created'] = 'pending'
    self.state_icon['queued'] = 'pending'
    self.state_icon['started'] = 'running'
    self.state_icon['passed'] = 'passed'
    self.state_icon['failed'] = 'failed'
    self.state_icon['errored'] = 'errored'
    self.state_icon['ready'] = 'pending'
  
  
  def get_gtk_icon(self, state):
    filename = 'job_{}.svg'.format(self.state_icon[state])
    pixbuf = gdkpixbuf.Pixbuf.new_from_file_at_size(filename, self.iconsizes[1], self.iconsizes[2])
    icon = gtk.Image.new_from_pixbuf(pixbuf)
    return icon
  
  def get_svg_icon(self, state):
    filename = 'job_{}.svg'.format(self.state_icon[state])
    directory = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(directory, filename)
  
  
  def _init_travis(self, auth_token):
    self.indicator.set_menu(self._load_menu())
    self.travis = travispy.TravisPy.github_auth(auth_token)
    
    # get travis data
    self.travis_user = self.travis.user()
    self.travis_repos = self.travis.repos(member=self.travis_user.login)
    
    self.builds = dict()
    for repo in self.travis_repos:
      self.builds[repo.slug] = dict()
      
      for build in self.travis.builds(slug=repo.slug):
        # create timestamps from strings
        if not build.started_at is None:
          build.started_at = dateutil.parser.parse(build.started_at)
        if not build.finished_at is None:
          build.finished_at = dateutil.parser.parse(build.finished_at)
        
        self.builds[repo.slug][int(build.number)] = build
        
  
  def update(self):
    while True:
      # get data and find changes
      self._travis_update()
      
      # apply the interface update
      gobject.idle_add(self.indicator.set_menu, self._main_menu())
      
      time.sleep(self.update_rate)
  

  def _travis_update(self):
    # get new data from API
    self.travis_repos = self.travis.repos(member=self.travis_user.login)
    
    changes = False
    
    for repo in self.travis_repos:
      for build in self.travis.builds(slug=repo.slug):
        n = int(build.number)

        build_changed = False

        # check for changes
        if not n in self.builds[repo.slug]:
          # new job
          label = self._build_label_str(build)
          repo_info = 'in {}'.format(repo.slug)
          notify.Notification.new("{} was created".format(label), repo_info, self.get_svg_icon(build.state)).show()
          
          build_changed = True
        elif self.builds[repo.slug][n].state != build.state:
          # status changed
          label = self._build_label_str(build)
          repo_info = 'in {}'.format(repo.slug)
          notify.Notification.new("{} {}".format(label, build.state), repo_info, self.get_svg_icon(build.state)).show()
          
          build_changed = True
        
        if build_changed:
          # create timestamps from strings
          if not build.started_at is None:
            build.started_at = dateutil.parser.parse(build.started_at)
          if not build.finished_at is None:
            build.finished_at = dateutil.parser.parse(build.finished_at)
          
          # update data for this build
          self.builds[repo.slug][int(build.number)] = build
          
          changes = True
    
    if changes:
      self._update_status()
  

  def _main_menu(self):
    # start menu build
    menu = gtk.Menu()
    
    now = datetime.datetime.utcnow()
    now = now.replace(tzinfo=pytz.utc)
    
    for repo in self.travis_repos:
      builds = [(self.builds[repo.slug][k], k) for k in self.builds[repo.slug] if self.builds[repo.slug][k].state in {'queued', 'started', 'ready', 'created'} or self._build_cmp_date(self.builds[repo.slug][k].finished_at, 7)]
      if len(builds) > 0:
        builds = sorted(builds, key=lambda b: b[1], reverse=True)
        menu.append(self._label_menu_item("{}".format(repo.slug), "https://travis-ci.org/{}".format(repo.slug)))
        
        for build, k in builds[:10]:
          
          # create time string
          if build.state == 'started' and not build.started_at is None:
            time_str = ' (started ' + timeago.format(build.started_at, now) + ')'
          elif build.state in {'passed', 'failed', 'errored'} and not build.finished_at is None:
            time_str = ' (' + timeago.format(build.finished_at, now) + ')'
          else: # build.state in {'pending', 'queued', 'ready'}
            time_str = ''
          
          #submenu = gtk.Menu()
          #for i in build.job_ids:
          #  job = self.travis.job(i)
          #  label = "#{} {}".format(job.number, job.config['os'])
          #  if "compiler" in job.config:
          #    label = label + "/" + job.config['compiler']
          #  submenu.append(self._image_menu_item(label, self.state_icon[job.state], "https://travis-ci.org/{}/jobs/{}".format(repo.slug, job.id)))
          
          label = self._build_label_str(build)
          
          menu.append(self._image_menu_item(label + time_str, self.get_gtk_icon(build.state), url="https://travis-ci.org/{}/builds/{}".format(repo.slug, build.id)))
          
        menu.append(self._seperator_menu_item())
      
    q = gtk.MenuItem("Quit")
    q.connect("activate", self.stop)
    menu.append(q)
    
    menu.show_all()
    return menu
  
  
  def _load_menu(self):
    menu = gtk.Menu()

    m = gtk.MenuItem('Loading...')
    m.set_sensitive(False)
    menu.append(m)
    
    menu.show_all()
    return menu
  
  
  def _image_menu_item(self, title, image=None, url=None, submenu=None):
    assert url is None or submenu is None
    
    m = gtk.ImageMenuItem(title)
    if not image is None:
      m.set_image(image)
      item_settings = m.get_settings()
      item_settings.set_property('gtk-menu-images', True)
    if not url is None:
      def open_url(unused): webbrowser.open(url)
      m.connect("activate", open_url)
    if not submenu is None:
      m.set_submenu(submenu)
    return m
  
  
  def _label_menu_item(self, label, url=None, submenu=None):
    assert url is None or submenu is None
    
    m = gtk.MenuItem(label)
    if not url is None:
      def open_url(unused): webbrowser.open(url)
      m.connect("activate", open_url)
    if not submenu is None:
      m.set_submenu(submenu)
    return m
  
  
  def _seperator_menu_item(self):
    return gtk.SeparatorMenuItem()
  
  
  def _check_menu_item(self, label, checked, action=None, action_param=None):
    m = gtk.CheckMenuItem(label)
    if not action is None:
      if not action_param is None:
        m.connect("toggled", action, action_param)
      else:
        m.connect("toggled", action)
    m.set_active(checked)
    return m
  
  
  def _update_status(self):
    builds = list()
    for repo in self.builds:
      for n in self.builds[repo]:
        builds.append(self.builds[repo][n])
    
    builds = [b for b in builds if b.commit.author_email == self.travis_user.email]
    builds_yellow = [b for b in builds if b.yellow]
    
    if len(builds_yellow) > 0:
      self.indicator.set_icon(os.path.abspath('logo_yellow.png'))
    else:
      builds = sorted([b for b in builds if not b.finished_at is None], key=lambda b: b.finished_at, reverse=True)
      
      if builds[0].green:
        self.indicator.set_icon(os.path.abspath('logo_green.png'))
      else:
        self.indicator.set_icon(os.path.abspath('logo_red.png'))
  
  
  def _build_label_str(self, build):
    # create label string
    if build.pull_request:
      return "[PR #{}] by {}".format(build.pull_request_number, build.commit.author_name)
    else:
      return "[{}] by {}".format(build.commit.branch, build.commit.author_name)
  
  
  def _build_cmp_date(self, date, days):
    if date is None:
      return False
    else:
      now = datetime.datetime.utcnow()
      now = now.replace(tzinfo=pytz.utc)
      delta = now - datetime.timedelta(days=days)
      return date > delta
  
  
  def stop(self, source):
    notify.uninit()
    gtk.main_quit()
  

def main():
  # load config
  config = configparser.ConfigParser()
  config.read('config.ini')
  
  indicator = Indicator(config['Github']['auth_token'], config['Github']['update_rate'])
  
  gobject.threads_init()
  signal.signal(signal.SIGINT, signal.SIG_DFL)
  gtk.main()

if __name__ == "__main__":
  main()
