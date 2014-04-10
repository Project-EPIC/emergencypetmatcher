$as_vagrant   = 'sudo -u vagrant -H bash -l -c'
$home         = '/home/vagrant'

Exec {
  path => ['/usr/sbin', '/usr/bin', '/sbin', '/bin']
}

# --- Preinstall Stage ---------------------------------------------------------

stage { 'preinstall':
  before => Stage['main']
}

class apt_get_update {
  exec { 'apt-get -y update':
    unless => "test -e ${home}/.rvm"
  }
}

class { 'apt_get_update':
  stage => "preinstall"
}

# --- Packages -----------------------------------------------------------------
package {['libssl1.0.0',
          'libssl-dev',
          'sqlite3', 
          'libsqlite3-dev',
          'curl', 
          'libpq-dev', 
          'git-core', 
          'ntp', 
          'nodejs',
          "mongodb-clients",
          "python-imaging"]:
  ensure => "installed"
}

# --- Nginx -----------------------------------------------------------------
class {"nginx": }

nginx::resource::upstream { 'gunicorn':
  ensure  => "present",
  members => ["127.0.0.1:8000"]
}

nginx::resource::vhost { 'project-vhost':
  ensure      => "present",
  index_files => [],
  proxy       => "http://gunicorn",
}

nginx::resource::location { 'project':
    ensure         => "present",
    location       => '/vagrant/deployment/static',
    location_alias => "/vagrant/deployment/static",
    vhost          => 'project-vhost',
}

#Get rid of Nginx Defaults.
file { "/etc/nginx/conf.d/default.conf":
  require => Package ["nginx"],
  ensure => "absent",
  notify => Service ["nginx"],
}

# --- Setup Python, VirtualEnv, Django, and Gunicorn -----------------------------------------------------------------


#Python
class { "python::dev": version => "2.7"}

#VirtualEnv
class { "python::venv": owner => "vagrant", group => "vagrant" }
python::venv::isolate {"/vagrant/project":
  requirements => "/vagrant/project/requirements.txt",
  version => "2.7.3"
}

#Gunicorn
class { "python::gunicorn": owner => "vagrant", group => "vagrant" }
python::gunicorn::instance { "epm":
  venv => "/vagrant/project",
  src => "/vagrant/project",
  django => true,
  django_settings => "settings.py",
} ->

#Startup Gunicorn
exec { "startup gunicorn":
  command => "${as_vagrant} 'cd /vagrant/project; source bin/activate; bash start_server.sh'",
}


# #Once Puppet has configured the environment, you need to run the following
# #commands manually:

# #  $python manage.py syncdb
# #  $python manage.py migrate home
# #  $python manage.py migrate social_auth
# #  $gunicorn --bind 0.0.0.0:8000 project.wsgi:application (listening on localhost:8000)














