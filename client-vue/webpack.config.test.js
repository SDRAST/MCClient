// for use with webpack v4
const path = require("path")

const { VueLoaderPlugin } = require('vue-loader')

module.exports = {
    mode: 'development',
    entry: [
        "./src/index.js"
    ],
    output: {
        filename: "bundle.js",
        path: path.resolve(__dirname, "dist")
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                include: path.resolve(__dirname, "src"),
                use: 'vue-loader'
            },
            {
                test: /\.js$/,
                include: path.resolve(__dirname, "src"),
                loader: "babel-loader"
            },
            {
                test: /\.css$/,
                loader: "null-loader"
            }

        ]
    },
    plugins: [
        new VueLoaderPlugin(),
    ],
    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js' // 'vue/dist/vue.common.js' for webpack 1
        }
    },
    // devtool:"source-map"
}
