const { defineConfig } = require("@vue/cli-service");
const path = require("path");
const resolve = (p) => path.join(__dirname, p);
module.exports = defineConfig({
  transpileDependencies: true,
  productionSourceMap: false,
  chainWebpack: (config) => {
    config.resolve.alias.set("@/", resolve("./src/"));
  },
  css: {
    loaderOptions: {
      less: {
        lessOptions: {
          modifyVars: {
            /* less 变量覆盖，用于自定义 ant design 主题 */
            "primary-color": "#12007B",
            "link-color": "#12007B",
            "border-radius-base": "4px",
            "link-hover-color": "#12007B",
          },
          javascriptEnabled: true,
        },
      },
    },
  },
  devServer: {
    // 设置代理
    host: "0.0.0.0", //
    port: 10000, //自定义端口
    https: false, //false关闭https，true为开启
    open: false, //自动打开浏览器
    proxy: {
      "/api": {
        target: "http://127.0.0.1:10001",
        // target: "http://localhost:10001", //本机调试
        // target: "http://43.139.112.84:10001", // 服务器测试
        changeOrigin: true,
      },
    },
  },
});
