import { createApp } from "vue";
import App from "./App.vue";
import Antd from "ant-design-vue";
import "ant-design-vue/dist/antd.less";
import router from "./router";
// eslint-disable-next-line @typescript-eslint/no-var-requires
// const axios = require("@/axios/index").default;
import axios from "@/axios/index";
import store from "./store";
import { message } from "ant-design-vue";
import { UploadOutlined } from "@ant-design/icons-vue";

const app = createApp(App);
app.config.globalProperties.$axios = axios;
app.config.globalProperties.$router = router;
app.config.globalProperties.$message = message;

app
  .use(store)
  .use(router)
  .use(Antd)
  .component("upload-outlined", UploadOutlined)
  .mount("#app");
