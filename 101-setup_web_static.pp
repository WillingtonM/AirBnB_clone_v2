#!/usr/bin/puppet apply
# AirBnB clone web server setup and configuration

exec { 'apt-get-update':
  command => '/usr/bin/apt-get update',
  path    => '/usr/bin:/usr/sbin:/bin',
}

exec { 'remove-current':
  command => 'rm -rf /data/web_static/current',
  path    => '/usr/bin:/usr/sbin:/bin',
}

package { 'nginx':
  ensure  => installed,
  require => Exec['apt-get-update'],
}

exec {'start nginx':
  provider => shell,
  command  => 'sudo service nginx start',
  before   => Exec['create test directory'],
}

exec {'create shared directory':
  provider => shell,
  command  => 'sudo mkdir -p /data/web_static/shared/',
  before   => Exec['create test directory'],
}

exec {'create test directory':
  provider => shell,
  command  => 'sudo mkdir -p /data/web_static/releases/test/',
  before   => Exec['add test content'],
}

exec {'add test content':
  provider => shell,
  command  => 'echo "
  <html>
    <head>
    </head>
    <body>
      Holberton School
    </body>
  </html>"> 
  /data/web_static/releases/test/index.html',
  before   => Exec['create symbolic link to current'],
}

exec {'create symbolic link to current':
  provider => shell,
  command  => 'sudo ln -sf /data/web_static/releases/test/ /data/web_static/current',
  before   => File['/data/'],
}

file {'/data/':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
  before  => Exec['serve current to hbnb_static'],
}

exec {'serve current to hbnb_static':
  provider => shell,
  command  => 'sed -i "61i\ \n\tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t\tautoindex off;\n\t}" /etc/nginx/sites-available/default',
  before   => Exec['restart nginx'],
}

file { '/var/www':
  ensure  => directory,
  mode    => '0755',
  recurse => true,
  require => Package['nginx'],
}

exec {'restart nginx':
  provider => shell,
  command  => 'sudo service nginx restart',
}