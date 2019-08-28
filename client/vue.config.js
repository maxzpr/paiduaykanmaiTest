const path = require("path");

module.exports = {
   publicPath: '/static/',
   outputDir: path.resolve(__dirname, "../server/app/static"),
   configureWebpack: (config) => {
      config.output.filename = '[name].[hash:8]js';
      config.output.chunkFilename = '[name].[hash:8].js';
   },
}