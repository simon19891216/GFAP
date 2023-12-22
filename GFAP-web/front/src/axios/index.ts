import axios from "axios";
import { message } from "ant-design-vue";

// Full config:  https://github.com/axios/axios#request-config
axios.defaults.baseURL =
  process.env.baseURL || process.env.apiUrl || "http://43.139.112.84:10001";
// axios.defaults.headers.common['Authorization'] = AUTH_TOKEN;
// axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
// axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*";

axios.defaults.headers["X-Requested-With"] = "XMLHttpRequest";
const config = {
  baseURL: "",
  timeout: 60000 * 1000, // Timeout
  withCredentials: true, // Check cross-site Access-Control
};
const _axios = axios.create(config);

_axios.interceptors.request.use(
  function (config: any) {
    if (config.headers["Content-Type"] == "") {
      config.headers["Content-Type"] = "application/json;charset=UTF-8";
    }
    return config;
  },
  function (error) {
    // Do something with request error
    return Promise.reject(error);
  }
);

// Add a response interceptor
// _axios.interceptors.response.use(
//   function (response) {
//     const headers = response.headers;
//     // 非json直接返回
//     if (
//       headers["content-type"] !== undefined &&
//       headers["content-type"] !== ""
//     ) {
//       if (headers["content-type"].indexOf("application/json") === -1) {
//         return response.data;
//       }
//     }

//     // Do something with response data
//     const state = response.data.code + "";
//     if (response.data.code && state != "0000") {
//       message.error(response.data.message);
//       return response;
//     } else {
//       return response;
//     }
//   },
//   function (error) {
//     // Do something with response error
//     if (error.response.status === 302) {
//       // 获取当前网页的url及参数
//       let redirect_uri = "";
//       if (window.location.href.split("?code").length >= 2) {
//         redirect_uri = window.location.href.split("?code")[0];
//       } else {
//         redirect_uri = window.location.href.split("&code")[0];
//       }
//       error.response.data.entity.redirectUrl;
//       // 跳转至sso认证页面
//       window.location.replace(
//         error.response.data.entity.redirectUrl + "&redirect_uri=" + redirect_uri
//       );
//     }
//     return Promise.reject(error);
//   }
// );

export default _axios;
