var util = {
    /**
    Map a value from one scale to another
    Args:
        val (Number): The number we wish to rescale
        range1 (Array): The scale of val
        range2 (Array): The array to which we want to scale
    */
    mapRange: function(val, range1, range2){
        var diff1 = range1[1] - range1[0];
        var diff2 = range2[1] - range2[0];
        var rel1 = (val - range1[0]) / diff1 ;
        var rel2 = diff2 * rel1 ;
        return rel2 + range2[0];
    },
    /**
    Given some input x value, compute a gaussian function with linear baseline,
    given some fit parameters.
    Args:
        x (Number): The value for which to calculate this function
        a (Number): Height of gaussian
        x0 (Number): Mean of gaussian
        sigma (Number): Standard deviation
        slope (Number): Slope of line component
        intercept (Number): Intercept of line component
    */
    gaussFunction: function(x, params){
        var [a, x0, sigma, slope, intercept] = params
        if (! slope){
            slope = 0.0;
        }
        if (! intercept){
            intercept = 0.0 ;
        }
        // var gaussPart = a*Math.exp(-Math.pow((x - x0), 2) / (2 * Math.pow(sigma,2)));
        // var linePart = (slope * x) + intercept;
        var val = a*Math.exp(-Math.pow((x - x0), 2) / (2 * Math.pow(sigma,2))) + (slope * x) + intercept
        // console.log(gaussPart, linePart, val);
        return val ;
    },

    /**
    Given some input x value, compute a linear output.
    Args:
        x (Number): The value for which to calculate this function
        a (Number): Height of gaussian
        x0 (Number): Mean of gaussian
        sigma (Number): Standard deviation
        slope (Number): Slope of line component
        intercept (Number): Intercept of line component
    */
    lineFunction: function(x, a, x0, sigma, slope, intercept){
        return slope * x + intercept;
    },
    /**
     * @function zeroPad
     * Taken from StackOverflow.
     * Pad a number with leading zeros.
     * @param  {Number} num    The number to pad with zeros
     * @param  {Number} places The total number of digits to have.
     * @return {String}        A zero padded version of num.
     */
    zeroPad: function(num, places) {
        var zero = places - num.toString().length + 1;
        return Array(+(zero > 0 && zero)).join("0") + num;
    },

    /**
     * @function displayTime
     * Given some number that represents a time in seconds,
     * return a string in 00:00:00 format
     * @param  {Number} timeInSeconds
     * @return {String} Formatted time string.
     */
    displayTime: function(timeInSeconds){
        var deltaTimeHours = Math.floor(timeInSeconds / 3600);
        var deltaTimeMinutes = Math.floor(timeInSeconds / 60) - (deltaTimeHours * 60);
        var displayTimeSeconds = timeInSeconds % 60 ;

        var displayTime = "{}:{}:{}".format(util.zeroPad(deltaTimeHours, 2),
                                            util.zeroPad(deltaTimeMinutes, 2),
                                            util.zeroPad(displayTimeSeconds, 2))
        return displayTime;
    },
    /**
     * @function rad2deg
     * Turn a degree in radians into degrees
     * @param {Number} rad - The number in radians
     */
    rad2deg(rad){
        if (rad.constructor !== Number){
            rad = parseFloat(rad, 10);
        }
        return rad * (180. / Math.PI);
    },


    /**
     * Turn a single radian value, or an array of radian values
     * into a formatted String or Array of formatted Strings, in degrees
     * @param  {Number/Array} val     [description]
     * @param  {[type]} options [description]
     * @return {[type]}         [description]
     */
    formatRad(val, options){
        if (val === undefined){
            throw `Argument is not a number or array`
        }
        if (options === undefined){
            options = {}
        }
        options = Object.assign({digits:2}, options)

        var converter = (v)=>{
            if (v === undefined){
                return ""
            }
            let deg = util.rad2deg(v)
            return deg.toFixed(options.digits)
        }

        if (val.constructor === Number){
            return converter(val)
        }else{
            return val.map(converter)
        }
    },


    getUTCTime(){
        var now = new Date();
        return `${now.getUTCHours()}:${now.getUTCMinutes()}:${now.getUTCSeconds()}`
    },

    /**
     *
     * @param  {[type]} str1 [description]
     * @param  {[type]} str2 [description]
     * @return {[type]}      [description]
     */
    strIn(str1, str2){
        var val = str1.indexOf(str2)
        if (val === -1){
            return false
        }else{
            return true
        }
    },

    /**
     * function that returns an array with values starting at start,
     * ending at end, incremented by increment
     * @param  {Number} start  start value
     * @param  {Number} end  end value
     * @param  {Number} increment increment value
     * @return {Array}
     */
    range(start, end, increment){
        if (increment == undefined){
            increment = 1.0
        }
        var nElements = Math.floor((end-start)/increment)
        var empty = new Array(nElements).fill(0) // have to fill to make it work
        return empty.map((x,i)=>{return start+(increment*i)})
    },

    /**
     * Return an object that can be iterated over.
     * @param  {[type]} start     [description]
     * @param  {[type]} end       [description]
     * @param  {[type]} increment [description]
     * @return {[type]}           [description]
     */
    rangeGen(start, end, increment){
        var gen = function*(){
            var val = start
            while (val < end){
                val += increment
                yield val
            }
        }
        var iter = {}
        iter[Symbol.iterator] = gen
        return iter
    }
}

export default util
