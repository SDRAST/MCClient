<script>
import * as log from "loglevel"

var logger = log.getLogger("SocketIOMixin")

export default {
    props:{
        "socket": {default: null, type:Object}
    },
    methods:{
        /**
         * Automatically add handler information to kwargs object.
         *
         * Assumes `handlerName` is an event already registered on socket
         * @param  {String} cmd  name of command to execute server-side
         * @param  {Array} args  args array send to Python method
         * @param  {Object} kwargs  kwargs object sent to Python method
         * @param  {String} handlerName name of handler that will be called
         *  client side
         * @return {null}
         */
        serverCommand(cmd, args, kwargs, handlerName){
            var time = new Date().toISOString()
            console.log(`SocketIOMixin.serverCommand: ${cmd} received at ${time}`)
            if (! this.socket.connected){
                console.log(`SocketIOMixin.serverCommand: not connected at ${time}`)
                return
            }
            if (kwargs === undefined){
                kwargs = {}
            }
            if (handlerName === ""){
                console.log(`SocketIOMixin.serverCommand: no cb handler for ${cmd}`)
                this.socket.emit(cmd, {"args":args, "kwargs":kwargs})
                return
            }else{
                console.log(`SocketIOMixin.serverCommand: ${cmd} handler is ${handlerName}`)
            }
            if ('cb_info' in kwargs){
                logger.warn("SocketIOMixin.serverCommand: cb_info object already present in kwargs. Not resetting.")
            }else{
                kwargs.cb_info = {
                    cb:handlerName
                }
            }
            this.socket.emit(cmd, {"args":args, "kwargs":kwargs})
        },
        getPort(socketOrPort){
            // console.log(`SocketIOMixin.getPort`)
            var port = socketOrPort
            if (typeof socketOrPort === "object" && socketOrPort !== null){
                if ("io" in socketOrPort){
                    port = parseInt(this.socket.io.opts.port)
                }
            }
            return port
        },
        registerPort(socketOrPort){
            var port = this.getPort(socketOrPort)
            this.port = port
            this.registeredPorts[port] = true
        },
        checkIfRegistered(socketOrPort){
            console.log(`SocketIOMixin.checkIfRegistered called`)
            var port = this.getPort(socketOrPort)
            if (port in this.registeredPorts){
                return true
            }
            return false
        },
        registerSocketHandlers(){},
        startTimers(){},
        getInitialData(){}
    },
    watch: {
        socket(){
            var time = new Date().toISOString()
            console.log(`SocketIOMixin: watch: socket event at ${time}`)
            if (! this.checkIfRegistered(this.socket)){
                console.log("SocketIOMixin: watch: socket re-registered")
                this.registerPort(this.socket)
                this.registerSocketHandlers()
            }
        }
    },
    mounted:function(){
        this.registerPort(this.socket)
        this.registerSocketHandlers()
        this.socket.on("connect",()=>{
            this.getInitialData()
            this.startTimers()
        })
    },
    data:function(){
        var port = -1
        if (this.socket !== null){
            port = parseInt(this.socket.io.opts.port)
        }
        return {
            "port":port,
            "registeredPorts":{port:false}
        }
    }
}
</script>
