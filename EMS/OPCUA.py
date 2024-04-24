from opcua import ua,Client

class OPCUA():
    def __init__(self):
        url = "opc.tcp://192.168.81.174:4840"
        # url = "opc.tcp://opcua:4840"
        # url = "opc.tcp://192.168.1.101:4840"
        self.client = Client(url)
        # self.security_string = "Basic256Sha256,SignAndEncrypt," + r"C:\Users\jan.hermanns\Desktop\Girea opc ua\Girea opcUA\cient_X.509 Certificate_4.der" + "," + r"C:\Users\jan.hermanns\Desktop\Girea opc ua\Girea opcUA\cient_X.509 Certificate_4.pem"
        self.security_string = "Basic256Sha256,SignAndEncrypt," + "my_cert2.der" + "," + "my_private_key2.pem"
        self.client.set_security_string(self.security_string)
        self._connect()
        self.json =self._get_server_stukur(self.client.get_objects_node())

    def __del__(self):
        self.client.disconnect()

    def pull_data(self):
        return self._data(pull=True)
        
    def push_data(self):
        self._data(push=True)

    def set_data(self):
        pass

    def _data(self, pull=False, push=False,  json=None):
        if json == None:
            json = self.json
        for a, b in json.items():
            if isinstance(b, dict):
                self._data(pull, push, json=b)
            elif isinstance(b, self._mytype):
                if pull:
                    b.pull_value()
                if push:
                    b.push_value()
            else:
                print("error data type:",type(b))
        return json

    def _connect(self):
        try:
            self.client.connect()
            self.client.load_type_definitions()
            print("Connected to OPC UA Server")
        except Exception as err:
            print("server not found")
            # sys.exit(1)

    def _get_server_stukur(self, node, json = {}):
        chillist = node.get_children()
        try:
            chillist.remove(self.client.get_node("i=2253"))
        except:
            pass
        for childId in chillist:
            ch = self.client.get_node(childId)
            if ch.get_node_class() == ua.NodeClass.Object:
                name = ch.get_browse_name().Name.split("_")[-1]
                json[name] = {}
                self._get_server_stukur(ch, json[name])
            elif ch.get_node_class() == ua.NodeClass.Variable:
                try:
                    name = ch.get_browse_name().Name.split("_")[-1]
                    # json[name] = ch.get_value()
                    json[name] = self._mytype(ch)
                except ua.uaerrors._auto.BadWaitingForInitialData:
                    pass
        return json

    class _mytype():
        def __init__(self, opc):
            self.opc = opc
            self.pull_value()
            self.type = type(self.value)
            self.newvalue = None

        def pull_value(self):
            self.value = self.opc.get_value()
        
        def push_value(self):
            if self.newvalue != None:
                self.opc.set_value(self.newvalue)
                self.newvalue = None

        def get_value(self):
            return self.value
        
        def set_value(self, newvalue):
            if self.value != newvalue:
                self.newvalue = newvalue

        def get_live(self):
            self.pull_value()
            return self.value
        
        def __str__(self):
            return str(self.value)