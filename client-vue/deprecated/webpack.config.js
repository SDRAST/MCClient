// works with webpack v3.11.0
const path = require("path");

var ExtractTextPlugin = require('extract-text-webpack-plugin')
var ExtractTextPluginConfig = new ExtractTextPlugin(
    "bundle.css"
)

module.exports = {
    entry: [
        "./src/index.js",
        "./src/index.css"
    ],
    output: {
        filename: "bundle.js",
        path: path.resolve(__dirname, "dist")
    },
    module: {
        rules: [
            {
                test: /\.css$/,
                include: [
                    path.resolve(__dirname, "node_modules"),
                    path.resolve(__dirname, "src")
                ],
                loader: ExtractTextPlugin.extract({
                    fallback:"style-loader",
                    use:"css-loader"
                })
            },
            {
                test: /\.vue$/,
                loader: 'vue-loader',
                include:[
                    path.resolve(__dirname, "src")
                ],
                options: {
                    loaders: {
                        // js: 'babel-loader!eslint-loader'
                        js: 'babel-loader'
                    }
                }
            }
        ]
    },
    plugins: [
        ExtractTextPluginConfig
    ],
    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js' // 'vue/dist/vue.common.js' for webpack 1
        }
    },
    devtool:"source-map"
}
