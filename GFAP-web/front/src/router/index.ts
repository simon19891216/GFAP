import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import Home from "../views/layout/index.vue";
import FormIndex from "@/views/form-demo/index.vue";
import GoKeggPFAMIndex from "@/views/annotation/go-kegg-pfam/index.vue";
import miRNAIncRNAIndex from "@/views/annotation/miRNA-IncRNA/index.vue";
import geneFamiles from "@/views/annotation/gene-families/index.vue";
import Statistics from "@/views/draw/statistics/index.vue";
import Pathway from "@/views/draw/pathway/index.vue";
import Translation from "@/views/other/translation/index.vue";
import RNA2DNA from "@/views/other/RNA2DNA/index.vue";
import Extraction from "@/views/other/extraction/index.vue";
import Conversion from "@/views/other/conversion/index.vue";
const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "home",
    component: Home,
    redirect: "/go-kegg-pfam-index",
    children: [
      {
        path: "/form-index",
        name: "form",
        component: FormIndex,
      },
      {
        path: "/annotation-index",
        name: "annotation",
        component: FormIndex,
      },
      {
        path: "/go-kegg-pfam-index",
        name: "go-kegg-pfam",
        component: GoKeggPFAMIndex,
      },
      {
        path: "/miRNA-IncRNA-index",
        name: "miRNA-IncRNA",
        component: miRNAIncRNAIndex,
      },
      {
        path: "/gene-families-index",
        name: "gene-families",
        component: geneFamiles,
      },
      {
        path: "/draw-index",
        name: "draw",
        component: FormIndex,
      },
      {
        path: "/statistics-index",
        name: "statistics",
        component: Statistics,
      },
      {
        path: "/pathway-index",
        name: "pathway",
        component: Pathway,
      },
      {
        path: "/translation-index",
        name: "translation",
        component: Translation,
      },
      {
        path: "/RNA2DNA-index",
        name: "RNA2DNA",
        component: RNA2DNA,
      },
      {
        path: "/extraction-index",
        name: "extraction",
        component: Extraction,
      },
      {
        path: "/conversion-index",
        name: "conversion",
        component: Conversion,
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
