<template>
  <div class="sub-menu-template">
    <TopBar />
    <div class="sub-menu-template-body">
      <div class="sub-menu-template-slider">
        <a-menu
          style="height: 100%"
          mode="inline"
          theme="dark"
          v-model:selectedKeys="selectedKeys"
        >
          <template v-for="(item, index) in list" :key="index">
            <a-sub-menu
              v-if="item.children"
              @titleClick="titleClick"
              :key="'sub_' + index"
            >
              <template #icon v-if="item.icon">
                <component :is="item.icon" />
              </template>
              <template #title>{{ item.label }}</template>
              <template v-for="(el, i) in item.children" :key="i">
                <a-sub-menu
                  v-if="el.children"
                  @titleClick="titleClick"
                  :key="'deepsub_' + i"
                >
                  <template #icon v-if="el.icon">
                    <component :is="el.icon" />
                  </template>
                  <template #title>{{ el.label }}</template>
                </a-sub-menu>
                <a-menu-item
                  v-else
                  :key="el.url || el.path || ''"
                  @click="handleClick(el)"
                >
                  <template #icon v-if="el.icon">
                    <component :is="el.icon" />
                  </template>
                  {{ el.label }}
                </a-menu-item>
              </template>
            </a-sub-menu>
            <a-menu-item
              v-else
              @click="handleClick(item)"
              :key="item.url || item.path || ''"
            >
              <template #icon v-if="item.icon">
                <component :is="item.icon" />
              </template>
              {{ item.label }}
            </a-menu-item>
          </template>
          <a-button
            type="text"
            @click="openPdf"
            block="true"
            style="font-weight: bold; color: floralwhite; font-size: large"
          >
            Cite
          </a-button>
        </a-menu>
      </div>
      <div class="sub-menu-template-content">
        <!-- 子路由 -->
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import TopBar from "./top-bar.vue";
export default {
  name: "Vue3Navigation",
  components: { TopBar },
  setup() {
    const openPdf = () => {
      window.open("https://doi.org/10.1093/plphys/kiad393", "_blank");
    };

    return {
      openPdf,
    };
  },
  data() {
    return {
      selectedKeys: [
        // "/form-index",
        "/go-kegg-pfam-index",
        // "/miRNA-IncRNA-index",
      ],
      list: [
        {
          label: "Annotation",
          path: "/form-index",
          children: [
            {
              label: "GO/KEGG/pfam",
              path: "/go-kegg-pfam-index",
            },
            {
              label: "miRNA-IncRNA",
              path: "/miRNA-IncRNA-index",
            },
            {
              label: "gene families",
              path: "/gene-families-index",
            },
          ],
        },
        {
          label: "Visualization",
          path: "/annotation-index",
          children: [
            {
              label: "statistics",
              path: "/statistics-index",
            },
            {
              label: "pathway",
              path: "/pathway-index",
            },
          ],
        },
        {
          label: "Auxiliary",
          path: "/annotation-index",
          children: [
            {
              label: "translation",
              path: "/translation-index",
            },
            {
              label: "RNA2DNA",
              path: "/RNA2DNA-index",
            },
            {
              label: "extraction",
              path: "/extraction-index",
            },
            {
              label: "conversion",
              path: "/conversion-index",
            },
          ],
        },
      ],
    };
  },
  methods: {
    handleClick(el) {
      this.$router.push(el.path);
    },
    titleClick(event) {
      console.log(event);
    },
  },
};
</script>
<style scoped lang="less">
@header-height: 68px;
@slider-width: 280px;

.sub-menu-template {
  display: flex;
  flex-direction: column;
  height: 100vh;
  min-width: 1200px;
  overflow: hidden;
}

.sub-menu-template-body {
  display: flex;
  flex: 1;
  background-color: #eee;
}

.sub-menu-template-slider {
  width: @slider-width;
  height: calc(100vh - @header-height);
  overflow-y: auto;
  border-right: 1px solid #f0f0f0;
}

.sub-menu-template-slider::-webkit-scrollbar {
  display: none;
}

.sub-menu-template-content {
  flex: 1;
  background-color: #efefef;
  padding: 16px;
}
</style>
