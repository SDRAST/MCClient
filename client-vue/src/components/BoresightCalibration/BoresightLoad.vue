<template>
    <div>
        <div class="boresight-load-container">
            <label>Year</label>
            <drop-down
                :contents="years"
                ref="year-drop-down"
                @drop-down-click="onYearDropDownClick">
            </drop-down>
            <label>Day of Year</label>
            <drop-down
                :contents="doys"
                ref="doy-drop-down"
                @drop-down-click="onDoyDropDownClick">
            </drop-down>
            <label>File Name</label>
            <drop-down
                :dropDownStyle="dropDownStyle"
                :contents="fileNames"
                ref="file-name-drop-down"
                @drop-down-click="onFileNameDropDownClick">
            </drop-down>
        </div>
        <button class="u-full-width no-bottom-margin" @click="onLoadButtonClick">Load</button>
        <hr/>
        <button class="u-full-width no-bottom-margin" @click="onMostRecentLoadButtonClick">Load Most Recent</button>
    </div>
</template>

<script>
import TableRow from "./../TableRow.vue"
import DropDown from "./../DropDown.vue"

export default {
    props:{
        filePaths: {type: Object, default: ()=>{return {}}}
    },
    components:{
        "table-row":TableRow,
        "drop-down":DropDown
    },
    methods:{
        updateYears(filePaths){
            this.years = Object.keys(filePaths)
            return this.years
        },
        onYearDropDownClick(year){
            this.doys = Object.keys(this.filePaths[year])
            this.doys.sort()
            return this.doys
        },
        onDoyDropDownClick(doy){
            var currentYear = this.$refs["year-drop-down"].displayVal.value
            this.fileNames = this.filePaths[currentYear][doy].map(
                (val)=>{return val[0]}
            )
            return this.fileNames
        },
        onFileNameDropDownClick(fileName){
        },
        onLoadButtonClick(){
            console.log(`BoresightLoad: onLoadButtonClick: called`)
            var currentYear = this.$refs["year-drop-down"].displayVal.value
            var currentDoy = this.$refs["doy-drop-down"].displayVal.value
            var currentFileNameIdx = this.$refs["file-name-drop-down"].idx
            try {
                var currentFilePath = this.filePaths[currentYear]
                                        [currentDoy]
                                        [currentFileNameIdx][1]
                this.$emit("load", currentFilePath)
            } catch (err) {
                console.log(`BoresightLoad: onLoadButtonClick: error ${err}`)
            }
        },
        onMostRecentLoadButtonClick(){
            console.log(`BoresightLoad: onMostRecentLoadButtonClick: called`)
            this.$emit("load-most-recent")
        }
    },
    watch: {
        filePaths(newFilePaths){
            this.updateYears(newFilePaths)
        }
    },
    data: function(){
        return {
            years: Object.keys(this.filePaths),
            doys: [],
            fileNames: [],
            dropDownStyle: {
                right: "0px",
                "min-width":"350px",
            }
        }
    }
}

</script>

<style scoped>

.boresight-load-container {
    display: grid;
    grid-template-columns: 1fr 2fr;
    grid-gap: 0.5rem;
    margin-bottom: 0.5rem;
}

.full-row {
    grid-column: 1 / 2;
}

.no-bottom-margin {
    margin-bottom: 0px;
}
</style>
