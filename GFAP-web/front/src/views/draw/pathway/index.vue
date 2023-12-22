<template>
  <div class="pathway-container">
    <a-form
      :layout="layout"
      :model="formState"
      v-bind="formItemLayout"
      @finish="onFinish"
      name="time_related_controls"
      @finishFailed="onFinishFailed"
      :rules="rules"
      :labelCol="{ offset: 0 }"
      :wrapperCol="{ offset: 0 }"
      style="height: 90vh; overflow: scroll"
    >
      <a-form-item name="upload" label="">
        <label style="color: red">* </label>
        <label>input annotation-result file</label>
        <a-upload-dragger
          v-model:file-list="formState['upload']"
          name="file"
          :max-count="1"
          :action="uploadAction"
          :before-upload="beforeUpload"
          :headers="uploadHeaders"
          @change="handleChange"
        >
          <p class="ant-upload-text">
            Click or drag file to this area to upload
          </p>
        </a-upload-dragger>
      </a-form-item>
      <div>or</div>
      <a-form-item name="gene_sequence">
        <a-textarea
          v-model:value="formState['gene_sequence']"
          placeholder="If you want to use the example data, the following parameters should be set as: GO, select closely related species: Arabidopsis_thaliana, type: biological_process"
          style="height: 15vh"
        >
        </a-textarea>
      </a-form-item>
      <a-form-item>
        <a-button
          type="primary"
          :loading="loading_data"
          style="width: 100%"
          @click="fillExampleGeneSequence"
        >
          using example data
        </a-button>
      </a-form-item>
      <a-form-item name="annotation_type" label="annotation type" style="">
        <a-radio-group
          v-model:value="formState['annotation_type']"
          :options="annotation_type_options"
        >
        </a-radio-group>
      </a-form-item>
      <a-form-item name="pvalue">
        <a-input
          style="width: 100%"
          v-model:value="formState['pvalue']"
          placeholder="the default value is 0.05"
          addon-before="p-value<="
        />
      </a-form-item>
      <a-form-item name="gene_number">
        <a-input
          style="width: 100%"
          v-model:value="formState['gene_number']"
          placeholder="the default value is 0"
          addon-before="gene number>="
        />
      </a-form-item>
      <a-form-item name="cut_value">
        <a-input
          style="width: 100%"
          v-model:value="formState['cut_value']"
          placeholder="the default value is 20"
          addon-before="cut value<="
        />
      </a-form-item>
      <a-form-item name="colormodel" label="select heatmap colormodel">
        <a-select
          v-model:value="formState['colormodel']"
          style="width: 100%"
          placeholder="select heatmap colormodel"
          :options="colormodel_options"
          @change="handleChange"
        >
        </a-select>
      </a-form-item>
      <a-form-item name="species" label="select closely related species">
        <a-select
          v-model:value="formState['species']"
          style="width: 100%"
          placeholder="select closely related species"
          :options="species_options"
          @change="handleChange"
        >
        </a-select>
      </a-form-item>
      <a-form-item name="go_category" label="Go category">
        <a-select
          v-model:value="formState['go_category']"
          style="width: 100%"
          :options="goCategory_option"
          placeholder="If input GO result"
          @change="handleChange"
        >
        </a-select>
      </a-form-item>
      <a-form-item name="email">
        <a-input
          style="width: 100%"
          v-model:value="formState['email']"
          placeholder="input an email for receiving results (optional)"
          addon-before="email"
        />
      </a-form-item>
      <a-form-item>
        <a-button
          type="primary"
          html-type="submit"
          :loading="loading"
          style="width: 100%"
        >
          draw (please open svg file using Adobe Illustrator)
        </a-button>
      </a-form-item>
      <!-- <a-form-item> <br /> </a-form-item> -->
      <a-form-item style="width: 50vw" v-if="output != null">
        <a-label> {{ output }} </a-label>
      </a-form-item>
    </a-form>
  </div>
</template>
<script>
import { example_gene_sequence } from "../../../static/annotation_result_file.ts";
import { species_options } from "../../../static/species_options.ts";
import { Modal } from "ant-design-vue";
import md5 from "js-md5";
export default {
  name: "form-demo",
  data() {
    return {
      // 表单数据 v-model
      formState: {
        sequence_type: "",
        gene_sequence: "",
        annotation_type: "",
        gene_number: null,
        pvalue: null,
        cut_value: null,
        species: "",
        database: "",
        colormodel: "",
        go_category: "",
        email: "",
        upload: [],
      },
      // 校验规则
      rules: {
        // upload: {
        //   type: "array",
        //   required: true,
        //   message: "Please select annotation file!",
        // },
        species: [
          {
            type: "string",
            required: true,
            message: "Please select closely related species",
          },
        ],
        database: [
          {
            type: "string",
            required: true,
            message:
              "Please select a database for annotating protein or CDS seqs",
          },
        ],
        sequence_type: {
          type: "string",
          required: true,
          message: "Please select sequence type!",
        },
        // go_category: {
        //   type: "string",
        //   required: true,
        //   message: "Please select GO catagory!",
        // },
        annotation_type: {
          type: "string",
          required: true,
          message: "Please select annotation type!",
        },
        // email: [
        //   {
        //     type: "string",
        //     required: true,
        //     message: "Please input your email address!",
        //   },
        // ],
      },
      layout: "vertical",
      formItemLayout: {},
      loading: false,
      output: null,
      result_image: null,
      file_tag: null,
      annotation_type_options: [
        { label: "GO", value: "-go" },
        { label: "KEGG", value: "-kegg" },
        { label: "protein domains", value: "-pfam" },
      ],
      other_output_types_options: [
        { label: "only GO/KEGG IDs", value: "-only_ID" },
      ],
      alignment_mode_options: [
        { label: "fast", value: "-am fast" },
        { label: "sensitive", value: "-am sensitive" },
      ],
      colormodel_options: [
        { value: "cy2bl" },
        { value: "lp2dp" },
        { value: "cy2p" },
        { value: "rcy2cy" },
        { value: "cy2bb" },
        { value: "lcy2dcy" },
        { value: "lg2cy" },
        { value: "lg2db" },
        { value: "r2cy" },
        { value: "lb2db" },
        { value: "r2g" },
        { value: "y2b" },
        { value: "r2b" },
        { value: "yrp" },
        { value: "y2cy" },
        { value: "y2p" },
        { value: "lr2dr" },
        { value: "lpk2dpk" },
        { value: "y2pur" },
        { value: "pur2b" },
        { value: "y2r" },
        { value: "dp2b" },
        { value: "o2cy" },
        { value: "y2db" },
        { value: "y2o" },
        { value: "y2lp" },
        { value: "o2r" },
        { value: "y2g" },
      ],
      species_options: [
        { value: "Abies_alba(Pinaceae)" },
        { value: "Abrus_precatorius(Fabaceae)" },
        { value: "Acer_yangbiense(Aceraceae)" },
        { value: "Actinidia_chinensis(Actinidiaceae)" },
        { value: "Aegilops_tauschii(Poaceae)" },
        { value: "Alyssum_linifolium(Brassicaceae)" },
        { value: "Amaranthus_hypochondriacus(Amaranthaceae)" },
        { value: "Amborella_trichopoda(Amborellaceae)" },
        { value: "Ananas_comosus(Bromeliaceae)" },
        { value: "Aquilegia_coerulea(Ranunculaceae)" },
        { value: "Arabidopsis_halleri(Brassicaceae)" },
        { value: "Arabidopsis_lyrata(Brassicaceae)" },
        { value: "Arabidopsis_thaliana(Brassicaceae)" },
        { value: "Arabis_alpina(Brassicaceae)" },
        { value: "Arachis_hypogaea(Brassicaceae)" },
        { value: "Arachis_ipaensis(Brassicaceae)" },
        { value: "Asparagus_officinalis(Liliaceae)" },
        { value: "Asparagus_setaceus(Liliaceae)" },
        { value: "Auxenochlorella_protothecoides(Chlorellaceae)" },
        { value: "Azolla_filiculoides(Salviniaceae)" },
        { value: "Bathycoccus_prasinos(Bathycoccaceae)" },
        { value: "Benincasa_hispida(Cucurbitaceae)" },
        { value: "Beta_vulgaris(Chenopodiaceae)" },
        { value: "Betula_platyphylla(Betulaceae)" },
        { value: "Boechera_stricta(Brassicaceae)" },
        { value: "Brachypodium_distachyon(Poaceae)" },
        { value: "Brachypodium_hybridum(Poaceae)" },
        { value: "Brachypodium_stacei(Poaceae)" },
        { value: "Brassica_carinata(Brassicaceae)" },
        { value: "Brassica_chinensis(Brassicaceae)" },
        { value: "Brassica_juncea(Brassicaceae)" },
        { value: "Brassica_napus(Brassicaceae)" },
        { value: "Brassica_nigra(Brassicaceae)" },
        { value: "Brassica_oleracea(Brassicaceae)" },
        { value: "Brassica_rapa(Brassicaceae)" },
        { value: "Cajanus_cajan(Fabaceae)" },
        { value: "Camelina_sativa(Brassicaceae)" },
        { value: "Camellia_sinensis(Theaceae)" },
        { value: "Cannabis_sativa(Cannabaceae)" },
        { value: "Capsella_grandiflora(Bignoniaceae)" },
        { value: "Capsella_rubella(Brassicaceae)" },
        { value: "Capsicum_annuum(Solanaceae)" },
        { value: "Capsicum_baccatum(Solanaceae)" },
        { value: "Capsicum_chinense(Solanaceae)" },
        { value: "Carica_papaya(Caricaceae)" },
        { value: "Carya_illinoinensis(Juglandaceae)" },
        { value: "Ceratodon_purpureus(Ditrichaceae)" },
        { value: "Chara_braunii(Characeae)" },
        { value: "Chenopodium_quinoa(Chenopodiaceae)" },
        { value: "Chimonanthus_praecox(Calycanthaceae)" },
        { value: "Chlamydomonas_reinhardtii(Chlamydomonadaceae)" },
        { value: "Chlorella_variabilis(Chlorellaceae)" },
        { value: "Chondrus_crispus(Gigartinaceae)" },
        { value: "Cicer_arietinum(Fabaceae)" },
        { value: "Citrullus_lanatus(Cucurbitaceae)" },
        { value: "Citrus_clementina(Rutaceae)" },
        { value: "Citrus_sinensis(Rutaceae)" },
        { value: "Citrus_unshiu(Rutaceae)" },
        { value: "Coccomyxa_subellipsoidea(Trebouxiophyceae)" },
        { value: "Coffea_canephora(Rubiaceae)" },
        { value: "Coffea_eugenioides(Rubiaceae)" },
        { value: "Corchirus_olitorius(Malvaceae)" },
        { value: "Corchorus_capsularis(Malvaceae)" },
        { value: "Corymbia_citriodora(Myrtaceae)" },
        { value: "Cucumis_melo(Cucurbitaceae)" },
        { value: "Cucumis_sativus(Cucurbitaceae)" },
        { value: "Cucurbita_argyrosperma(Cucurbitaceae)" },
        { value: "Cucurbita_moschata(Cucurbitaceae)" },
        { value: "Cucurbita_pepo(Cucurbitaceae)" },
        { value: "Cyanidioschyzon_merolae(Galdieriaceae)" },
        { value: "Cynara_cardunculus(Compositae)" },
        { value: "Daucus_carota(Apiaceae)" },
        { value: "Dendrobium_catenatum(Orchidaceae)" },
        { value: "Dendrobium_officinale(Orchidaceae)" },
        { value: "Dioscorea_alata(Dioscoreaceae)" },
        { value: "Dioscorea_cayenensis(Dioscoreaceae)" },
        { value: "Durio_zibethinus(Malvaceae)" },
        { value: "Elaeis_guineensis(Arecaceae)" },
        { value: "Ensete_ventricosum(Musaceae)" },
        { value: "Eragrostis_curvula(Poaceae)" },
        { value: "Eragrostis_tef(Poaceae)" },
        { value: "Eremochloa_ophiuroides(Poaceae)" },
        { value: "Erigeron_canadensis(Compositae)" },
        { value: "Erythranthe_guttata(Phrymaceae)" },
        { value: "Eucalyptus_grandis(Myrtaceae)" },
        { value: "Eutrema_salsugineum(Brassicaceae)" },
        { value: "Fragaria_ananassa(Rosaceae)" },
        { value: "Fragaria_vesca(Rosaceae)" },
        { value: "Galdieria_sulphuraria(Cyanidiaceae)" },
        { value: "Ginkgo_biloba(Ginkgoaceae)" },
        { value: "Glycine_max(Fabaceae)" },
        { value: "Glycine_soja(Fabaceae)" },
        { value: "Gnetum_montanum(Gnetaceae)" },
        { value: "Gossypium_hirsutum(Malvaceae)" },
        { value: "Gossypium_raimondii(Malvaceae)" },
        { value: "Handroanthus_impetiginosus(Bignoniaceae)" },
        { value: "Helianthus_annuus(Compositae)" },
        { value: "Herrania_umbratica(Fabaceae)" },
        { value: "Hevea_brasiliensis(Euphorbiaceae)" },
        { value: "Hibiscus_syriacus(Malvaceae)" },
        { value: "Hordeum_vulgare(Poaceae)" },
        { value: "Hylocereus_undatus(Cactaceae)" },
        { value: "Ipomoea_nil(Convolvulaceae)" },
        { value: "Ipomoea_triloba(Convolvulaceae)" },
        { value: "Jatropha_curcas(Euphorbiaceae)" },
        { value: "Juglans_regia(Juglandaceae)" },
        { value: "Kalanchoe_fedtschenkoi(Crassulaceae)" },
        { value: "Kalanchoe_laxiflora(Crassulaceae)" },
        { value: "Kandelia_obovata(Rhizophoraceae)" },
        { value: "Lactuca_sativa(Compositae)" },
        { value: "Leersia_perrieri(Poaceae)" },
        { value: "Lindenbergia_philippensis(Orobanchaceae)" },
        { value: "Linum_usitatissimum(Linaceae)" },
        { value: "Liriodendron_chinense(Magnoliaceae)" },
        { value: "Lobularia_maritima(Brassicaceae)" },
        { value: "Lotus_japonicus(Fabaceae)" },
        { value: "Lupinus_albus(Fabaceae)" },
        { value: "Lupinus_angustifolius(Fabaceae)" },
        { value: "Macadamia_integrifolia(Proteaceae)" },
        { value: "Manihot_esculenta(Euphorbiaceae)" },
        { value: "Marchantia_polymorpha(Marchantiaceae)" },
        { value: "Medicago_truncatula(Fabaceae)" },
        { value: "Micromonas_commoda(Mamiellaceae)" },
        { value: "Micromonas_pusilla(Mamiellaceae)" },
        { value: "Mimulus_guttatus(Phrymaceae)" },
        { value: "Miscanthus_sinensis(Fabaceae)" },
        { value: "Momordica_charantia(Cucurbitaceae)" },
        { value: "Monoraphidium_neglectum(Sphaeropleales)" },
        { value: "Morus_notabilis(Moraceae)" },
        { value: "Musa_acuminata(Musaceae)" },
        { value: "Nelumbo_nucifera(Nymphaeaceae)" },
        { value: "Nicotiana_attenuata(Solanaceae)" },
        { value: "Nicotiana_tabacum(Solanaceae)" },
        { value: "Nymphaea_colorata(Nymphaeaceae)" },
        { value: "Olea_europaea(Oleaceae)" },
        { value: "Oropetium_thomaeum(Poaceae)" },
        { value: "Oryza_sativa(Poaceae)" },
        { value: "Ostreococcus_lucimarinus(Bathycoccaceae)" },
        { value: "Ostreococcus_tauri(Bathycoccaceae)" },
        { value: "Panicum_hallii(Poaceae)" },
        { value: "Panicum_virgatum(Poaceae)" },
        { value: "Papaver_somniferum(Papaveraceae)" },
        { value: "Petunia_axillaris(Solanaceae)" },
        { value: "Phalaenopsis_equestris(Orchidaceae)" },
        { value: "Pharus_latifolius(Poaceae)" },
        { value: "Phaseolus_acutifolius(Fabaceae)" },
        { value: "Phaseolus_vulgaris(Papilionaceae)" },
        { value: "Phoenix_dactylifera(Arecaceae)" },
        { value: "Phyllostachys_heterocycla(Fabaceae)" },
        { value: "Physcomitrella_patens(Funariaceae)" },
        { value: "Picea_abies(Pinaceae)" },
        { value: "Pinus_lambertiana(Pinaceae)" },
        { value: "Pinus_taeda(Pinaceae)" },
        { value: "Piper_nigrum(Piperaceae)" },
        { value: "Pistacia_vera(Anacardiaceae)" },
        { value: "Poncirus_trifoliata(Rutaceae)" },
        { value: "Populus_bolleana(Salicaceae)" },
        { value: "Populus_deltoides(Salicaceae)" },
        { value: "Populus_euphratica(Salicaceae)" },
        { value: "Populus_trichocarpa(Salicaceae)" },
        { value: "Portulaca_amilis(Portulacaceae)" },
        { value: "Prosopis_alba(Poaceae)" },
        { value: "Prunus_avium(Rosaceae)" },
        { value: "Prunus_dulcis(Rosaceae)" },
        { value: "Prunus_persica(Rosaceae)" },
        { value: "Punica_granatum(Punicaceae)" },
        { value: "Pyrus_x_bretschneideri(Rosaceae)" },
        { value: "Quercus_lobata(Fagaceae)" },
        { value: "Quercus_rubra(Fagaceae)" },
        { value: "Quercus_suber(Fagaceae)" },
        { value: "Raphanus_sativus(Brassicaceae)" },
        { value: "Rhodamnia_argentea(Myrtaceae)" },
        { value: "Ricinus_communis(Euphorbiaceae)" },
        { value: "Rosa_chinensis(Rosaceae)" },
        { value: "Rosa_rugosa(Rosaceae)" },
        { value: "Saccharum_spontaneum(Poaceae)" },
        { value: "Salix_purpurea(Salicaceae)" },
        { value: "Salvia_splendens(Lamiaceae)" },
        { value: "Schrenkiella_parvula(Brassicaceae)" },
        { value: "Selaginella_moellendorffii(Selaginellaceae)" },
        { value: "Sequoia_sempervirens(Taxodiaceae)" },
        { value: "Sesamum_indicum(Pedaliaceae)" },
        { value: "Setaria_italica(Poaceae)" },
        { value: "Setaria_viridis(Poaceae)" },
        { value: "Solanum_lycopersicum(Solanaceae)" },
        { value: "Solanum_pennellii(Solanaceae)" },
        { value: "Solanum_tuberosum(Solanaceae)" },
        { value: "Sorghum_bicolor(Poaceae)" },
        { value: "Spinacia_oleracea(Chenopodiaceae)" },
        { value: "Spirodela_polyrhiza(Lemnaceae)" },
        { value: "Synechocystis_sp.pcc(Chroococcaceae)" },
        { value: "Tarenaya_hassleriana(Capparaceae)" },
        { value: "Theobroma_cacao(Malvaceae)" },
        { value: "Trifolium_pratense(Fabaceae)" },
        { value: "Triticum_aestivum(Poaceae)" },
        { value: "Urochloa_fusca(Poaceae)" },
        { value: "Utricularia_gibba(Lentibulariaceae)" },
        { value: "Vaccinium_macrocarpon(Ericaceae)" },
        { value: "Vigna_angularis(Fabaceae)" },
        { value: "Vigna_radiata(Fabaceae)" },
        { value: "Vigna_unguiculata(Fabaceae)" },
        { value: "Vitis_vinifera(Vitaceae)" },
        { value: "Volvox_carteri(Pseudoviridae)" },
        { value: "Xanthoceras_sorbifolium(Sapindaceae)" },
        { value: "Zea_mays(Poaceae)" },
        { value: "Zingiber_officinale(Zingiberaceae)" },
        { value: "Ziziphus_jujuba(Rhamnaceae)" },
        { value: "Zostera_marina(Zosteraceae)" },
      ],
      goCategory_option: [
        { value: "biological_process" },
        { value: "cellular_component" },
        { value: "molecular_function" },
      ],
    };
  },
  computed: {
    uploadAction() {
      return "/api/upload?tag=" + this.file_tag;
    },
    // 上传文件地址及请求头
    uploadHeaders() {
      return {
        authorization: "authorization-text",
      };
    },
  },
  methods: {
    validateFileOrInput() {
      const upload = this.formState["upload"];
      const igs = this.formState["gene_sequence"];
      console.log(upload);
      console.log(igs);
      if ((!upload || upload.length === 0) && igs.trim() === "") {
        return false;
      }
      if (upload != null && upload.length != 0 && igs.trim() != "") {
        this.$message.info(
          "There are multiple types of inputs. We will handle the input content (instead of the input file) for finishing the related function."
        );
      }
      return true;
    },
    validateGOCatagory() {
      const annotation_type = this.formState["annotation_type"];
      const go_category = this.formState["go_category"];
      console.log(annotation_type);
      console.log(go_category);
      if (annotation_type.includes("-go") && go_category.trim() === "") {
        return false;
      }
      return true;
    },
    onFinish(values) {
      let body = { ...values };
      console.log("onFinish:", body);
      // 校验输入或者文件上传
      const validateRes = this.validateFileOrInput();
      if (!validateRes) {
        (this.loading_a1 = false), (this.loading_a2 = false);
        this.$message.error(
          "You should either upload a sequence file or directly input sequence string!"
        );
        return;
      }
      // body["tag"] = this.file_tag;
      if (
        this.formState.gene_sequence &&
        this.formState.gene_sequence.trim() != ""
      ) {
        body["tag"] = md5(this.formState.gene_sequence);
      } else {
        body["tag"] = this.file_tag;
      }
      if (this.validateGOCatagory() == false) {
        this.$message.error(`Please select GO catagory!`);
        return;
      }
      delete body["upload"];
      this.loading = true;
      this.$axios
        .post("/api/pathway", body)
        .then((res) => {
          console.log("res:", res);
          if (res.data.command.endsWith(".svg")) {
            this.result_image = res.data.output;
          }
          this.showConfirm(res.data.url);
          this.formState = {};
        })
        .catch((error) => {
          this.loading = false;
          var rsp = error.response;
          console.log("err data :", rsp.data);
          Modal.error({
            title: "Oops!",
            content: rsp.data.error,
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
    onFinishFailed(err) {
      console.log("Failed:", err.error);
    },
    beforeUpload(file) {
      console.log("beforeUpload:", file);
      this.file_tag = md5(file.uid);
      return true;
      // console.log("beforeUpload:", file);
      // const isLt1M = file.size / 1024 / 1024 < 1;
      // if (!isLt1M) {
      //   this.$message.error(`file must smaller than 1MB!`);
      // }
      // // this.file_tag = file.uid;
      // this.file_tag = md5(file.uid);
      // return isLt1M;
    },
    handleChange(info) {
      if (info.file == null) {
        return;
      }
      if (info.file.status !== "uploading") {
        console.log(info.file, info.fileList);
      }
      if (info.file.status === "done") {
        console.log(info.file);
        this.$message.success(`${info.file.name} file uploaded successfully`);
      } else if (info.file.status === "error") {
        this.$message.error(`${info.file.name} file upload failed.`);
      }
    },
    fillExampleGeneSequence() {
      this.formState.gene_sequence = example_gene_sequence;
    },
    showConfirm(attchement_url) {
      Modal.confirm({
        title: "Finished!",
        content: "Click 'Download' to get result file(s)!",
        okText: "Download",
        onOk() {
          console.log("OK");
          window.open(attchement_url, "_self");
        },
        onCancel() {
          console.log("Cancel");
        },
        class: "confirm",
      });
    },
  },
};
</script>
<style lang="less" scoped>
.form-demo {
  &-container {
    padding: 20px;
    height: 100%;
    background-color: #fff;
  }
}
.my-label-class label {
  color: red;
  font-weight: bold;
}
.ant-form-item {
  margin: 0 0 12px;
}
</style>
