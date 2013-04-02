* Layout
    +-------------------------------+
    |           header              |
    +-------------------------------+
    |           menu                |
    +-------------------------------+
    |          workspace            |
    +-------------------------------+
    |           footer              |
    +-------------------------------+

 
* Menu
  Menu locates under header section and above workspace section.
  It contains several menu tabs. 
    
    | Home | Account | Login |
    +-------------------------------------------------
  Home - leads to start_view. showing the order list of today.
  Account - list the user's account info. should be grayed out before login.
  Login - leads to login_view.
 
* db layerout.
  
   

* Session handling.
  
  data structure:
  There are 2 kinds of data structure used in session handling, timer wheel and session.
  
  session is a python dict with 2 contant key-value entries.
  session = { 
      'session_id' : 'sess_xxx',         #id of session. followed the pattern 
      'session_ref_counter' : 0，        #number of ref from timer wheel.
      ...
  }
  
  timer wheel is a python dict with 24 constant key-value entries.
  timer_wheel = {
      'session_tmout_0' : ['sess_1', 'sess_2', ... ],       #slot for sessions who will expiry during 00:00:00 ~ 00:59:59
      'session_tmout_1' : ['sess_311','sess_455', ...],     #slot for 01:00:00 ~ 01:59:59
      ...
      'session_tmout_23' : []                               #slot for 23:00:00 ~ 23:59:59
  }
  
  storage:
  session is stored in SAE kvdb. the key for kvdb entry is the the value of session_id. the value of kvdb entry is the session's serilized string using json format.
      import json
      from sae import kvdb
      def save_session( session ):
          key = session['session_id']
          value = json.dumps(session)
          kvc = kvdb.KVClient()
          kvc.add(key, value)
      
      def load_session( sess_id ):
          kvc = kvdb.KVClient()
          s = kvc.get(sess_id)
          return json.loads(s)
          
  timer wheel is stored in SAE kvdb. each time slot is stored as a kvdb entry.
      from sae import kvdb
      
      class TimerWheel(object):
          def __getitem__(self, key):
              kvc = KVClient()
              kvc.get(key)
          
          def __setitem__(self, key, item):
              kvc = KVClient()
              kvc.set(key, item)
              
  
  session id generation:
  since SAE python do not support counter. use memcached incr() to generate the session id.
       import pylibmc
       def genSessionId():
           mc = pylibmc.Client()
           if None == mc.get('newgo_session_id_gen'):
              mc.set('newgo_session_id_gen', 1)
           return 'session_%d' % mc.incr('newgo_session_id_gen')
  
  expiry of timeout session:
  the max idle time for a session is 1 hour.
  when create/fetch a session 
  
  
  
          
  