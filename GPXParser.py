#!/usr/bin/env python
import os, re
 
class GPXTrack:
   def __init__(self):
      self.attribs = {}
      self.wpts = []
 
   def from_string(self, c):
      f = re.search("<trk(?P<opts>.*?)>(?P<content>.*?)</trk>", c, re.DOTALL+re.I)   
      opts = re.findall(re.compile(".*?=\".*?\"", re.DOTALL), f.group("opts"))
      for opt in opts:
         n, v = opt.split("=")    
         v = v.strip()
         if v.startswith("\"") and v.endswith("\""): v = v[1:-1]
         self.attribs[n.strip()] = v
 
      segs = re.findall(re.compile("<trkseg>.*?</trkseg>", re.DOTALL+re.I), f.group("content"))   
      cont = re.sub(re.compile("<trkseg>.*</trkseg>", re.DOTALL+re.I), "",f.group("content"))
 
      attrib = re.findall(re.compile("<(.+?)>(.*?)</(.+?)>", re.DOTALL+re.I), cont)   
      for a in attrib:
         self.attribs[a[0].strip()] = a[1].strip()    
 
      for seg in segs:
         points = re.findall(re.compile("<trkpt.+?>.*?</trkpt>", re.DOTALL+re.I), seg)   
         for p in points:
            w = GPXWaypoint()    
            w.from_string(p.strip())
            self.wpts.append(w)
 
   def __repr__(self):
      r = "Track:   "+self.attribs.__repr__()+"\nPoints: "
      for w in self.wpts:
         r += w.__repr__() 
      return r+"\n"   
 
 
 
class GPXWaypoint:
   #lon = 0 # -180.0 - +180.0
   #lat = 0 # -90.0 - +90.0
   #attribs = {}
   def __init__(self, lon=0, lat=0):
      self.lon, self.lat = lon, lat 
      self.attribs={}
   def from_string(self, c):
      f = re.search("<(trk|w)pt(?P<opts>.*?)>(?P<content>.*?)</(trk|w)pt>", c, re.DOTALL+re.I)   
      if not f: return 1
      opts = re.findall(re.compile(".*?=\".*?\"", re.DOTALL), f.group("opts"))
      for o in opts:
         n, v = o.split("=")    
         v = v.strip()
         if v.startswith("\"") and v.endswith("\""): v = v[1:-1]
         if n.strip() == "lon": self.lon = float(v)
         elif n.strip() == "lat": self.lat = float(v)
      attrib = re.findall(re.compile("<(.+?)>(.*?)</(.+?)>", re.DOTALL+re.I), f.group("content"))   
      for a in attrib:
         self.attribs[a[0].strip()] = a[1].strip()    
 
   def __str__(self):
      return "WP (lon="+str(self.lon)+", lat="+str(self.lat)+")\n  Attributes: "+self.attribs.__repr__()+"\n"
   def __repr__(self):
      return self.__str__()
 
 
 
 
class GPXRoute:
   #wps = [] # list of GPXWaypoints    
   #attribs = {}
   def __init__(self):
      self.wps = [] # list of GPXWaypoints    
      self.attribs = {}
      pass    
 
class GPXParser:
   #trcks  = [] # list of GPXTrack objects    
   #wpts = [] # list of GPXWp objects    
   #rts  = [] # list of GPXRoute objects    
   def __init__(self, filename):    
      self.attribs={}
        if not filename.endswith(".gpx"):    
         print "Warning: filename does not end on .gpx..."
      self.file = filename    
      f = open(filename, "r")
      content = f.read(); f.close()
      self.init_from_string(content)
 
   def init_from_string(self, c):
      self.trcks, self.wpts, self.rts = [], [], []    
      gpx = re.search("<gpx(?P<opts>.*?)>(?P<content>.*?)</gpx>", c,re.DOTALL+re.I)   
      if not gpx: return 1
      gpx_opts = re.findall(re.compile(".*?=\".*?\"", re.DOTALL), gpx.group("opts"))
      for gopt in gpx_opts:
         n, v = gopt.split("=")    
         v = v.strip()
         if v.startswith("\"") and v.endswith("\""): v = v[1:-1]
         self.attribs[n.strip()] = v
 
      # Waypoints
      gpx_wpts = re.findall(re.compile("<wpt.*?>.*?</wpt>", re.DOTALL+re.I), gpx.group("content"))   
      for wp in gpx_wpts:
         wpt = GPXWaypoint()
         wpt.from_string(wp)
         self.wpts.append(wpt)
 
      # Tracks   
      gpx_trks = re.findall(re.compile("<trk.*?>.*?</trk>", re.DOTALL+re.I), gpx.group("content"))   
      for trk in gpx_trks:
         t = GPXTrack()
         t.from_string(trk)
         self.trcks.append(t)
 
 
 
 
if __name__=='__main__':
   import sys
   
   # parser = GPXParser("rondane06_tracks.gpx")    
   # parser = GPXParser("test.gpx")    

   parser = GPXParser(sys.argv[1])

   print parser.trcks
   for p in parser.wpts:
      print p
