<template>
  <div>
    <div class="container">
      <panel header="NMC Workstation" size="medium">
          <div class="workstation">
              <!-- show the current workstation and site if selected -->
              <label v-show="currentWorkstation !== null">Current Workstation: <span v-html="currentWorkstation"></span></label>
              <label v-show="currentSite !== null">Current Site: <span v-html="currentSite"></span></label>
              <!-- site and workstation selection -->
              <label>Site</label>
              <input-drop-down ref="site-drop-down" :contents="sites"></input-drop-down>
              <label>Workstation</label>
              <input-drop-down ref="workstation-drop-down" :contents="workstations"></input-drop-down>
              <button class="full-row" @click="onConnectClick">Connect</button>
          </div>
      </panel>
      <div>
        <center>
          <h6 class="superhead">Radio Astronomy Monitor and Control</h6>
          Time: Client: {{clientTime}}, Server ({{server}}): {{serverTime}}
          <div class="activity" style="width:500px">
            <!-- Project: <input class="superhead" v-model="project" value="TAMS" type="text" /> -->
            <label>Project</label>
            <drop-down ref="proj-drop-down"
                       :contents="projects"
                       :value="project"
                       @drop-down-click="onProjectDropDownClick"></drop-down>
            <label>Activity</label>
            <drop-down ref="act-drop-down"
                       :contents="activities"
                       :value="activity"
                       @drop-down-click="onActivityDropDownClick"></drop-down>
          </div>
          Project: {{project}}, Activity: {{activity}}
        </center>
      </div>
      <panel header="Pages" size="medium">
        <div class="pagemenu">
          <!-- The double quotes are required for 'to': "'...'" -->
          <!--
          <router-link :to="'/plan'" target="_blank">Planning Page</router-link><br/>
          <router-link :to="'/cal'" target="_blank">Calibration</router-link><br/>
          <router-link :to="'/pow'" target="_blank">Power Meter Monitor</router-link>
          <hr/>
          -->
          <router-link :to="'/plan'">Planning Page</router-link><br/>
          <router-link :to="'/cal'">Calibration</router-link><br/>
          <router-link :to="'/pow'">Power Meter Monitor</router-link><br/>
          <!--  v-link short form is : -->
          <router-link v-bind:to="'/old'" target="_blank">Legacy Page</router-link>
        </div>
      </panel>
    </div>
  </div>
</template>

<script>
  import Panel from "./Panel.vue"
  import InputDropDown from "./InputDropDown.vue"
  import DropDown from "./DropDown.vue"

  import * as log from "loglevel"
  import util from "./../util.js"

  var logger = log.getLogger("App")
  logger.debug("SuperHeader: logger created")

  export default {
    props:{
      // this is the computer clock time on the client
      clientTime: {type: String, default: null},
      // this is the computer clock time on the server
      serverTime: {type: String, default: null},
      server:     {type: String, default: null},
      project:    {type: String, default: null},
      projects:   {type: Array,  default: () => []},
      activities: {type: Array,  default: () => []},
      activity:   {type: String, default: null}
    },
    components:{
      "panel": Panel,
      "input-drop-down": InputDropDown,
      "drop-down": DropDown
    },
    //eforeUpdate(){
      //logger.debug("SuperHead.beforeUpdate: invoked")
      //bus.$emit('superHeadRendered', null)
    //},
    methods:{
      onConnectClick: function(){
          var site = this.$refs["site-drop-down"].displayVal.value
          var ws = this.$refs["workstation-drop-down"].displayVal.value
          this.connectToWorkstation(site, ws)
      },
      onProjectDropDownClick(project){
          // emits 'projectChanged' which is handled by App
          logger.debug(`SuperHeader.onProjectDropDownClick: ${project}`)
          var newProject = project
          bus.$emit('projectChanged', newProject)
      },
      onActivityDropDownClick(activity){
          // emits 'activityChanged' which is handled by App
          logger.debug(`SuperHeader.onActivityDropDownClick: ${activity}`)
          var newActivity = activity
          bus.$emit('activityChanged', newActivity)
      }
    },
    data: function(){
      return{
        sites: ["CDSCC","GDSCC","MDSCC"],
        workstations: [{display:"0 (simul)", value:0}].concat([91,92]).concat(util.range(1,10)),
        currentWorkstation: null,
        currentSite: null,
        antennaSimulated: null,
        onsource: null
      }
    }
  }
</script>

<style scoped>
.container {
    display: grid;
    grid-template-columns: 2fr 6fr 2fr;
    grid-gap: 0.5rem 0.5rem;

    .container button{
        margin-bottom: 0.0rem;
    }
}

.container button{
    margin-bottom: 0.0rem;
}

.full-row {
    grid-column: 1 / 3;
}

.workstation {
    display: grid;
    grid-template-columns: 0.4fr 1fr;
    grid-gap: 0.5rem;
}

.activity {
    display: grid;
    grid-template-columns: 0.4fr 1fr 0.4fr 1fr;
    grid-gap: 0.5rem;
}
</style>

<style>
.superhead{
  height: 1.25rem;
  .container {
      display: grid;
      grid-template-columns: 2fr 6fr 2fr;
      grid-gap: 0.5rem 0.5rem;
  }
  .pagemenu{
      border-style: solid;
  }
}
</style>
