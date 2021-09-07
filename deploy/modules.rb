#!/usr/bin/env ruby

require 'set'

environ = Set[]
Dir.glob('environments/*.yaml').each do |fn|
  File.foreach(fn) do |line|
    # Find lines between the `whitelist:` key and the next pure hash key
    if line =~ /^\s*whitelist:\s*$/ .. line =~ /^\s*[^-w ].*:\s*$/
      if /^\s*-\s*(?<quote>['"]?)(?<pkg>.*)\k<quote>$/ =~ line
        environ.add(pkg)
      end
    end
  end
end

dumped = false
File.foreach('configs/modules.yaml') do |line|
  if /^(?<prefix>\s*)blacklist:\s$/ =~ line
    unless dumped
      puts "#{prefix}whitelist:"
      environ.sort.each do |pkg|
        puts "#{prefix}  - #{pkg}"
      end
      dumped = true
    end
  end
  puts line
end
