#!/usr/bin/env ruby

require 'set'

environ = Set[]
Dir.glob('configs/**/modules.yaml').each do |fn|
  File.foreach(fn) do |line|
    if line =~ /^\s*whitelist:\s*$/../^\s*blacklist:\s*$/
      if /^\s*-\s*(?<quote>['"]?)(?<pkg>.*)\k<quote>$/ =~ line
        environ.add(pkg)
      end
    end
  end
end

dumped = false
File.foreach('configs/applications/modules.yaml') do |line|
    if line =~ /^\s*whitelist:\s*$/../^\s*blacklist:\s*$/
      if /^(?<prefix>\s*-\s*)(?<quote>['"]?)(?:.*)\k<quote>$/ =~ line
        unless dumped
          environ.sort.each do |pkg|
            puts "#{prefix}#{pkg}"
          end
          dumped = true
        end
      else
        puts line
      end
    else
      puts line
    end
end
