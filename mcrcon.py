#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket, select, struct, re

def cleanup(text): # because the results try to create colours and therefore have horrible characters in them
    return(text.replace("§c","").replace("§a","").replace("§6","").replace("§4","").rstrip())

class MCRcon:
    def __init__(self, host, port, password):
        self.cmds = dir(self)[3:14]+dir(self)[16:]
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((host, port))
            self.send_real(3, password)
        except: raise Exception("Could not connect to server")
    def close(self):
        self.s.close()
    
    def send(self, command):
        return self.send_real(2, command)
    
    def send_real(self, out_type, out_data):
        #Send the data
        buff = struct.pack('<iii', 10+len(out_data), 0, out_type) + out_data + "\x00\x00"
        self.s.send(buff)
        
        #Receive a response
        in_data = ''
        ready = True
        while ready:
            #Receive an item
            tmp_len, tmp_req_id, tmp_type = struct.unpack('<iii', self.s.recv(12))
            tmp_data = self.s.recv(tmp_len-8) #-8 because we've already read the 2nd and 3rd integer fields

            #Error checking
            if tmp_data[-2:] != '\x00\x00':
                raise Exception('protocol failure', 'non-null pad bytes')
            tmp_data = tmp_data[:-2]
            
            #if tmp_type != out_type:
            #    raise Exception('protocol failure', 'type mis-match', tmp_type, out_type)
           
            if tmp_req_id == -1:
                raise Exception('auth failure')
           
            m = re.match('^Error executing: %s \((.*)\)$' % re.escape(out_data), tmp_data)
            if m:
                raise Exception('command failure', m.group(1))
            
            #Append
            in_data += tmp_data

            #Check if more data ready...
            ready = select.select([self.s], [], [], 0)[0]
        
        return in_data

    def status(self):
        if self.__init__() == None: ok = True
        else: ok = False
        return(ok)
    def stop(self):
        return(self.send("stop"))
    def users(self):
        output = cleanup(self.send("list")).split(" ")
        return({'number':int(output[2]),'names':output[10:],'max':int(output[6])})
    def ls(self):
        return(self.users())
    def cmd(self,command):
        return(self.send(command))
    def reload(self):
        return(self.send("reload"))
    def version(self):
        return(self.send("version"))
    def say(self,message):
        return(self.send("say" + str(message)))
    def save(self,mode="all"):
        return(self.send("save-%s" % str(mode)))
    def time(self,newTime):
        return(cleanup(self.send("time set %s world" % str(newTime))))
    def day(self):
        return(self.time("day"))
    def whitelist(self,action,user=None):
	actions = ["add","remove","reload","on","off"]
	if action not in actions: raise Exception("Unknown command %s %s" % (str(action),str(user)))
	else:
		if user: return(cleanup(self.send("whitelist %s %s" % (str(action),str(user)))))
		else: return(cleanup(self.send("whitelist %s" % str(action))))
    def night(self):
        return(self.time("night"))
    def weather(self,newWeather):
        return(cleanup(self.send("weather world %s" % str(newWeather))))
    def clear(self):
        return(cleanup(self.weather("clear")))
    def op(self,user):
        return(cleanup(self.send("op %s" % str(user))))
    def deop(self,user):
        return(self.send("deop %s" % str(user)))
    def stats(self):
        output = cleanup(self.send("uptime"))
        stats_out = {}
        stats_out['status'] = self.status()
        stats_out['uptime'] = {'days': int(output[1]),'hours': int(output[3]),'minutes': int(output[5])}
        stats_out['TPS'] = int(str(output[9]).split("\n")[0])
        stats_out['mem'] = {'max': int(output[11]), 'allocated': int(output[14]), 'free': int(output[17])} # in MB
        stats_out['users'] = self.users()
        return(stats_out)
