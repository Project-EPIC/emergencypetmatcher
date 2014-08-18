exec { "apt-get_update":
    command     => "/usr/bin/apt-get update",
    tries       => 3
}

exec { "apt-get_upgrade":
    command     => "/usr/bin/apt-get -y upgrade",
    require     => [ Exec["apt-get_update"] ],
    tries       => 3,
    refreshonly => true
}

group { 'puppet':   ensure => present }

#Misc. Packages.
$packages = ["make", "wget", "gcc"]
package { $packages: ensure => "installed"}


#PostgreSQL
class { "postgresql::server":
  listen_addresses => "*"
}

postgresql::server::db { 'epm_db':
  user     => 'epm_login',
  password => postgresql_password('epm_login', '3m3rgEncY'),
}

postgresql::server::db { 'test_epm_db':
  user     => 'epm_login',
  password => postgresql_password('epm_login', '3m3rgEncY'),
  owner    => "epm_login"
}

postgresql::server::role { "epm_login":
  createdb   => true
}

postgresql::server::pg_hba_rule { 'allow application network to access app database':
  description => "Open up postgresql for access from 192.168.50.5/24",
  type => 'host',
  database => 'epm_db',
  user => 'epm_login',
  address => '192.168.50.5/24',
  auth_method => 'md5',
}


#MongoDB
class { "::mongodb::server":
  # auth => true,
  ensure => "present",
  port => 27017,
  verbose => true,
  bind_ip => ["127.0.0.1", "192.168.50.6"]
}

mongodb_database { "epm_db":
  ensure => "present",
  tries => 10,
  require => Class["mongodb::server"]
}

# mongodb_user { "epm_login":
#   ensure        => present,
#   password_hash => mongodb_password('epm_login', '3m3rgEncY'),
#   database      => "epm_db",
#   roles         => ['readWrite', 'dbAdmin'],
#   tries         => 10,
#   require       => Class['mongodb::server'],
# }

