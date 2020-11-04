import Vue from "vue"
import io from "socket.io-client"
import { assert } from "chai"

import BoresightCalibration from "../src/components/BoresightCalibration/BoresightCalibration.vue"
import testScanningBoresightFileAnalyzer from "./testScanningBoresightFileAnalyzer.js"
import testSteppingBoresightFileAnalyzer from "./testSteppingBoresightFileAnalyzer.js"

function renderComponent(Component, propsData){
    var constructor = Vue.extend(Component)
    var vm = new constructor({propsData: propsData}).$mount()
    return vm
}

describe("BoresightCalibration", function(){
    it("has a mounted hook", function(){
        assert.typeOf(BoresightCalibration.mounted, "function")
    })

    it("sets correct default data", function(){
        var defaultData = BoresightCalibration.data()
        assert.include(
            defaultData,
            {type: "scanning"},
            "default data includes a boresight type"
        )
    })

    describe("mounted", function(){
        var [domain, port] = ["localhost", 5000]
        var socket = null
        var vm = null

        // var testSteppingFilePath = [
        //     "/home/dean/jpl-dsn/post-obs/boresight_data/2018/133/",
        //     "stepping_one_direction_boresight_results_2018-133-08h18m05s.hdf5"
        // ].join("")
        // var testSteppingFileName = "stepping_one_direction_boresight_results_2018-133-08h18m05s.hdf5"
        var testSteppingFilePath = testSteppingBoresightFileAnalyzer.file_path
        var testSteppingFileName = testSteppingBoresightFileAnalyzer.file_name

        var testScanningFilePath = testScanningBoresightFileAnalyzer.file_path
        var testScanningFileName = testScanningBoresightFileAnalyzer.file_name

        before(function(done){
            socket = io.connect(`http://${domain}:${port}`)
            socket.on("connect", ()=>{
                done()
            })
        })
        beforeEach(function(done){
            vm = renderComponent(BoresightCalibration, {"socket":socket})
            Vue.nextTick(()=>{
                done()
            })
        })
        afterEach(function(done){
            socket.removeAllListeners(
                "get_boresight_analyzer_object_handler")
            socket.removeAllListeners(
                "get_most_recent_boresight_analyzer_object_handler")
            vm.$destroy()
            done()
        })
        after(function(){
            socket.close()
        })
        it("sets test scanning file analyzer object", function(done){
            vm.analyzerObject = Object.assign({}, testScanningBoresightFileAnalyzer)
            Vue.nextTick(()=>{
                assert.isTrue(
                    vm.$refs["boresight-report"]
                      .$refs["channel-selector-el"]
                      .directions.right.show
                )
                assert.equal(
                    vm.$refs["boresight-report"].fileName,
                    testScanningFileName
                )
                done()
            })
        })
        it("sets test stepping file analyzer object", function(done){
            vm.analyzerObject = Object.assign({}, testSteppingBoresightFileAnalyzer)
            Vue.nextTick(()=>{
                assert.isTrue(
                    vm.$refs["boresight-report"]
                      .$refs["channel-selector-el"]
                      .directions.right.show
                )
                assert.equal(
                    vm.$refs["boresight-report"].fileName,
                    testSteppingFileName
                )
                done()
            })

        })
        it("loads a scanning analyzer object", function(done){
            var handler = (data)=>{
                console.log("get_boresight_analyzer_object_handler (scanning): called")
                Vue.nextTick(()=>{
                    assert.equal(
                        vm.analyzerObject.file_name,
                        testScanningFileName
                    )
                    done()
                })
            }
            socket.once("get_boresight_analyzer_object_handler", handler)
            vm.onLoad(testScanningFilePath)
        })
        it("loads a stepping analyzer object", function(done){
            var handler = (data)=>{
                console.log("get_boresight_analyzer_object_handler (stepping): called")
                console.log(data.args[0].file_name)
                Vue.nextTick(()=>{
                    assert.equal(
                        vm.analyzerObject.file_name,
                        testSteppingFileName
                    )
                    done()
                })
            }
            socket.once("get_boresight_analyzer_object_handler", handler)
            vm.onLoad(testSteppingFilePath)
        })
        it("loads most recent analyzer object", function(done){
            var handler = (data)=>{
                console.log("get_most_recent_boresight_analyzer_object_handler: called")
                Vue.nextTick(()=>{
                    assert.isDefined(
                        vm.analyzerObject.file_name
                    )
                    done()
                })
            }
            socket.once(
                "get_most_recent_boresight_analyzer_object_handler",
                handler
            )
            vm.onLoadMostRecent()
        })
    })
})
