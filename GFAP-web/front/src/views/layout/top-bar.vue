<template>
  <div class="sub-menu-template-header">
    <div class="sub-menu-template-logocon">
      <div class="sub-menu-template-logo" />
    </div>

    <div class="sub-menu-template-headcon">
      <span class="sub-menu-template-headtitle">{{ systemName }}</span>
    </div>
    <a-button type="primary" @click="openPdf" shape="circle">
      <question-outlined />
    </a-button>
  </div>
</template>

<script>
import axios from "@/axios/index";
import { QuestionOutlined } from "@ant-design/icons-vue";
export default {
  setup() {
    const openPdf = () => {
      window.open("https://maipdf.com/doc/a19746786054@pdf", "_blank");
    };

    return {
      openPdf,
    };
  },
  name: "TopBar",
  components: {
    QuestionOutlined,
  },
  data() {
    return {
      systemName: "GFAP---Gene Functional Annotation for Plants",
      systemMenuData: [],
    };
  },
  methods: {},
};
</script>
<style scoped lang="less">
@header-height: 68px;
@slider-width: 280px;
.sub-menu-template-header {
  display: flex;
  height: @header-height;
  line-height: @header-height;
}
.sub-menu-template-logocon {
  height: 100%;
  width: @slider-width;
}
.sub-menu-template-logo {
  width: 100%;
  height: 100%;
  background: url("@/assets/GFAP.png") no-repeat center;
  background-size: contain;
}
.sub-menu-template-headcon {
  flex: 1;
  background-color: #fff;
  border-bottom: 1px solid #f0f1f2;
}
.sub-menu-template-headtitle {
  font-size: 24px;
  font-weight: 600;
}
.sub-menu-template-headRight {
  float: right;
  display: flex;
  font-size: 16px;
  height: 100%;
}
.sub-menu-template-item {
  display: inline-block;
  padding: 0 20px;
  height: 100%;
  cursor: pointer;
  box-sizing: border-box;
  border-bottom: 1px solid transparent;
}
.sub-menu-template-item:hover {
  color: @primary-color;
  border-bottom-color: @primary-color;
}
.sub-menu-template-selfitem {
  width: 150px;
  padding: 8px 24px;
  font-size: 16px;
}
.sub-menu-template-uerinfocon {
  display: flex;
  align-items: center;
  height: 64px;
  padding: 0 16px;
  cursor: pointer;
}
.sub-menu-template-username {
  margin-left: 12px;
  font-size: 16px;
  line-height: 1.5;
}
</style>
