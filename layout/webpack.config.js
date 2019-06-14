const path = require("path");
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const webpackMode = require('webpack-mode');

let output_filename = "[name].[hash]";
if (webpackMode.isDevelopment) output_filename = "[name].dev";

module.exports = {
  entry: { main: "./src/js/main.js", hp: "./src/js/hp.js", 
           investments: "./src/js/investments.js", investment: "./src/js/investment.js" },
           //aboutus: "./src/js/about-us.js", contacts: "./src/js/contacts.js"},
  devtool: 'source-map',
  output: {
    path: path.resolve(__dirname, "dist"),
    path: path.resolve("./static/bundles/"),
    filename: output_filename + ".js"
  },
  plugins: [
    new CleanWebpackPlugin({ dry: webpackMode.isDevelopment }),
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
        use: ['file-loader?name=images/[name].[ext]']
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
