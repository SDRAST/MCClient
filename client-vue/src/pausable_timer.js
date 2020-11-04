class PausableTimer{
    constructor(callback, waitTime){
        this.callback = callback
        this.waitTime = waitTime
        this.running = false
        this.paused = false
        this.timer = null
    }
    start(){
        this.callback()
        this.timer = setInterval(this.callback, this.waitTime)
        this.running = true
    }
    pause(){
        if (this.paused){return}
        if (! this.running){return}
        clearInterval(this.timer)
        this.paused = true
    }
    stop(){
        clearInterval(this.timer)
        this.running = false
    }
    unpause(){
        if (this.paused){
            this.start()
        }
    }
    running(){
        return this.running
    }
    paused(){
        return this.paused
    }
}

export default PausableTimer
