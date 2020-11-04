<template>
</template>

<script>
</script>

<style scoped>
.slider {
    position:relative;
    z-index: 1;
    margin-left: 0.0rem;
    margin-right: 0.0rem;
    width: 100%;
    height:2.0rem;
}

.slider button {
    border-radius: 25px;
    width: 20px;
    height: 20px ;
    padding: 0;
    top: 0px;
    position: relative;
    background-color: white;
}

.slider:before{
    border-top: 2px solid #dfdfdf;
    content:"";
    margin: 0 auto; /* this centers the line to the full width specified */
    position: absolute; /* positioning must be absolute here, and relative positioning must be applied to the parent */
    top: 50%; left: 0; right: 0; bottom: 0;
    width: 100%;
    z-index: -1;
}
</style>
