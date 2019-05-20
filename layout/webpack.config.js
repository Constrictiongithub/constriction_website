const path = require("path");
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const webpackMode = require('webpack-mode');

let output_filename = "[name].[hash]";
if (webpackMode.isDevelopment) output_filename = "[name].dev";

module.exports = {
  entry: { main: "./src/js/main_entry.js", chartist: "./src/js/chartist_entry.js", rangeslider: "./src/js/rangeslider_entry.js" },
  output: {
    path: path.resolve(__dirname, "dist"),
    path: path.resolve("./static/bundles/"),
    filename: output_filename + ".js"
  },
  plugins: [
    new CleanWebpackPlugin(),
    new BundleTracker({ filename: "./webpack-stats.json" }),
    new MiniCssExtractPlugin({
      filename: output_filename + ".css"
    }),
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
      "window.jQuery": "jquery"
    }),
  ],
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      },
      {
        test: /\.scss$/,
        exclude: /node_modules/,
        use: [
          MiniCssExtractPlugin.loader,
          "css-loader",
          "postcss-loader",
          "sass-loader"
        ]
      },
      {
        test: /\.(woff(2)?|ttf|eot|svg)(\?v=[\d\.])?/,
        use: [{
          loader: 'file-loader',
          options: {
            name: '[name].[ext]',
            outputPath: 'fonts/'
          }
        }]
      },
      {
        test: /\.(jpe?g|png|gif|svg)$/i,
        use: [
          "file-loader?name=images/[name].[ext]",
          "image-webpack-loader?bypassOnDebug"
        ]
      }
    ]
  }
};
