import Vue from "vue"
import io from "socket.io-client"
import * as log from "loglevel"
//import VueRouter from "./../node_modules/vue-router"
//import Routes from "./routes"
import VueGoogleCharts from './../node_modules/vue-google-charts/'
import App from "./components/App.vue"

// use packages
//Vue.use(VueRouter)
Vue.use(VueGoogleCharts)

var __version__ = "1.6.0"

var logLevels = {
    "App":"DEBUG",
    "SocketIOMixin": "DEBUG",
    "BoresightCalibration": "DEBUG",
    "BoresightReport":"DEBUG",
    "Nodding":"DEBUG"
}

Object.keys(logLevels).forEach((loggerName)=>{
    log.getLogger(loggerName).setLevel(logLevels[loggerName])
})

// Register routes
//const router = new VueRouter({
//    routes: Routes
//});

var init = ()=>{
    var [domain, port] = ["localhost", 5000]
    var app = new Vue({
        components:{
            "app":App
        },
        data: {
            "domain":domain,
            "port":port,
            "version":__version__
        },
        el: "#main",
        template:`<app ref="app" :domain="domain" :port="port" :version="version"></app>`,
        //router: router
    })
    return app
}
var bus = new Vue({})
window.bus = bus

var app = init()

export default app
