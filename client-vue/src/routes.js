import Home              from './components/Home.vue'
import Planning          from './components/Planning.vue'
import Calibr            from './components/Calibr.vue'
import App               from './components/App.vue'
import AppOld            from './components/AppOld.vue'
import SourceMonitor     from './components/SourceMonitor.vue'
import AntennaMonitor    from './components/AntennaMonitor.vue'
import PowerMeterMonitor from './components/PowerMeterMonitor.vue'

export default [
    {path: '/',     component: Home,              name: "home"},
    {path: '/plan', component: Planning,          name: "plan"},
    {path: '/cal',  component: Calibr},
    // has old code ...
    {path: '/old',  component: AppOld,            name: "old"},
    // placeholders
    {path: '/ant',  component: AntennaMonitor},
    {path: '/pow',  component: PowerMeterMonitor}
]
