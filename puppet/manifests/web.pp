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
          "libjpeg-dev",
          "zlib1g-dev",
          "libpng12-dev",
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
  members => ["127.0.0.1:8889"]
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

nginx::resource::location { "project-media":
  ensure        => "present",
  location      => "/vagrant/media",
  location_alias  => "/vagrant/media",
  vhost           => "project-vhost"
}

# --- Setup Python, VirtualEnv, Django, and Gunicorn -----------------------------------------------------------------

#Python
class { 'python':
  version    => 'system',
  pip        => true,
  dev        => true,
  virtualenv => true,
  gunicorn   => false,
}

python::requirements { '/vagrant/project/requirements.txt':
  virtualenv => '/vagrant/project',
  owner      => 'vagrant',
  group      => 'vagrant',
}

