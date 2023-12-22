<template>
  <div class="geneFamilies-container">
    <a-form :layout="layout" style="height: 90vh; overflow: scroll">
      <a-form
        :layout="layout"
        :model="formState"
        v-bind="formItemLayout"
        style="border: 2px solid rgb(235, 250, 250)"
        @finish="showSingle"
        name="time_related_controls"
        @finishFailed="onFinishFailed"
        :rules="rules"
      >
        <h2
          style="
            border: 0px solid rgb(225, 0, 0);
            font-weight: bold;
            color: red;
          "
        >
          Show Members of a Single Family
        </h2>
        <!-- <a-form-item name="gene_sequence" label="Gene Sequence">
          <a-textarea
            v-model:value="formState['gene_sequence']"
            placeholder="directly input the gene sequence"
            style="width: 50vw"
            :rows="2"
          />
        </a-form-item> -->
        <a-form-item name="upload" label="">
          <label>input </label>
          <label style="color: red">*</label>
          <label>protein-fasta</label>
          <label style="color: red">* </label>
          <label>file</label>
          <a-upload-dragger
            v-model:file-list="formState['upload']"
            name="file"
            :max-count="1"
            :action="uploadAction"
            :before-upload="beforeUpload"
            :headers="uploadHeaders"
            @change="handleChange"
            style="height: 1vw"
          >
            <!-- <p class="ant-upload-drag-icon">
              <inbox-outlined></inbox-outlined>
            </p> -->
            <p class="ant-upload-text">
              Click or drag file to this area to upload
            </p>
          </a-upload-dragger>
        </a-form-item>
        <div>or</div>
        <a-form-item name="gene_sequence">
          <a-textarea
            v-model:value="formState['gene_sequence']"
            placeholder="if you want to use the example data, the gene family should be set “ARF (Auxin response factors)”"
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
        <a-form-item
          name="factor_type"
          label="select transcription factor or gene family"
        >
          <a-select
            v-model:value="formState['factor_type']"
            mode="species"
            style="width: 100%"
            placeholder="select closely transcription factor or gene family"
            :options="factor_options"
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
        <!-- <a-form-item
          name="sequence_type"
          label="Please select one of the following choices if you want to identify the members of all families"
        >
          <a-radio-group v-model:value="formState['sequence_type']">
            <a-radio :value="'-atf'">transcription factor</a-radio>
            <a-radio :value="'-agf'">gene family</a-radio>
          </a-radio-group>
        </a-form-item> -->
        <a-form-item>
          <a-button
            type="primary"
            html-type="submit"
            :loading="loading_a1"
            style="width: 100%"
            @click="null"
          >
            show members of a single family
          </a-button>
        </a-form-item>
      </a-form>
      <br />
      <a-form
        :layout="layout"
        :model="formState"
        v-bind="formItemLayout"
        style="border: 2px solid rgb(235, 250, 250)"
        @finish="showDomain"
        name="time_related_controls"
        @finishFailed="onFinishFailed"
        :rules="rules"
      >
        <h2
          style="
            border: 0px solid rgb(225, 0, 0);
            font-weight: bold;
            color: red;
          "
        >
          Show Genes Containing Domains of Families
        </h2>
        <a-form-item name="upload1" label="">
          <label>input </label>
          <label style="color: red">*</label>
          <label>protein-fasta</label>
          <label style="color: red">* </label>
          <label>file</label>
          <a-upload-dragger
            v-model:file-list="formState['upload1']"
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
        <a-form-item name="gene_sequence1">
          <a-textarea
            v-model:value="formState['gene_sequence1']"
            placeholder="directly input protein-fasta example"
            style="height: 15vh"
          >
          </a-textarea>
        </a-form-item>
        <a-form-item>
          <a-button
            type="primary"
            :loading="loading_data"
            style="width: 100%"
            @click="fillExampleGeneSequence1"
          >
            using example data
          </a-button>
        </a-form-item>
        <!-- <a-form-item
          name="factor_type"
          label="select closely transcription factor or gene family"
        >
          <a-select
            v-model:value="formState['factor_type']"
            mode="species"
            style="width: 100%"
            placeholder="select closely transcription factor or gene family"
            :options="factor_options"
            @change="handleChange"
          >
          </a-select>
        </a-form-item> -->
        <a-form-item name="email">
          <a-input
            style="width: 100%"
            v-model:value="formState['email']"
            placeholder="input an email for receiving results (optional)"
            addon-before="email"
          />
        </a-form-item>
        <a-form-item
          name="sequence_type"
          label="Please select one of the following choices if you want to identify the members of all families"
        >
          <a-radio-group v-model:value="formState['sequence_type']">
            <a-radio :value="'-atf'">transcription factor</a-radio>
            <a-radio :value="'-agf'">gene family</a-radio>
          </a-radio-group>
        </a-form-item>
        <a-form-item>
          <a-button
            type="primary"
            html-type="submit"
            :loading="loading_a2"
            style="width: 100%"
            @click="null"
          >
            show genes containing domains of families
          </a-button>
        </a-form-item>
        <a-form-item> <br /> </a-form-item>
        <a-form-item style="width: 50vw" v-if="output != null">
          <a-label> {{ output }} </a-label>
        </a-form-item>
      </a-form>
    </a-form>
  </div>
</template>
<script>
import { example_gene_sequence } from "../../../static/protein_fasta_file.ts";
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
        gene_sequence1: "",
        evalue: "",
        match_percentage: "",
        species: "",
        upload: [],
        upload1: [],
        factor_type: "",
      },
      // 校验规则
      rules: {
        factor_type: [
          {
            type: "string",
            required: true,
            message: "Please select a family!",
          },
        ],
        sequence_type: {
          type: "string",
          required: true,
          message: "Please select annotation type!",
        },
      },
      layout: "vertical",
      formItemLayout: {},
      loading_data: false,
      loading_a1: false,
      loading_a2: false,
      output: null,
      file_tag: null,
      factor_options: [
        { label: "------------------transcription factor------------------" },
        { label: "AP2 (APETALA2)", value: "AP2" },
        { value: "AP2ERF" },
        {
          label: "ARR (Arabidopsis response regulators)",
          value: "ARR",
        },
        { label: "ARF (Auxin response factors)", value: "ARF" },
        { value: "B3" },
        {
          label: "BBR-BPC (barley B-recombinant/basic pentacysteine)",
          value: "BBR-BPC",
        },
        { label: "BES1 (BRI1-EMS-SUPPRESSOR 1)", value: "BES1" },
        { label: "bHLH (basic Helix-Loop-Helix)", value: "bHLH" },
        { label: "bZIP (basic leucine zipper)", value: "bZIP" },
        {
          label: "CAMTA (calmodulin binding transcription activator)",
          value: "CAMTA",
        },
        { label: "CO (CONSTANS)", value: "CO" },
        { label: "CPP (cystein-rich polycomb)", value: "CPP" },
        { label: "DBB (double B-box zinc finger)", value: "DBB" },
        { label: "E2FDP (Early 2 factor)", value: "E2FDP" },
        { label: "EIL (EIN3-like)", value: "EIL" },
        { label: "FAR1 (FAR‐RED‐IMPAIRED RESPONSE1)", value: "FAR1" },
        { label: "G2-like (GARP superfamily)", value: "G2-like" },
        { value: "GATA" },
        {
          label: "GRAS (gibberellic acid insensitive)",
          value: "GRAS",
        },
        { label: "GRF (Growth regulating-factors)", value: "GRF" },
        {
          label: "HB-PHD (homeobox and protein domain, the homeodomain)",
          value: "HB-PHD",
        },
        { label: "HB (homeobox)", value: "HB" },
        {
          label: "HSF (heat shock transcription factor)",
          value: "HSF",
        },
        {
          label: "LBD (lateral organ boundaries domain)",
          value: "LBD",
        },
        { label: "LFY (LEAFY)", value: "LFY" },
        { value: "MADS" },
        { value: "MYB" },
        { label: "NAC (NAM, ATAF1/2, and CUC2)", value: "NAC" },
        { value: "NFYA" },
        { value: "NFYB" },
        { value: "NOZZLE" },
        { label: "RAV (ABI3/VP1)", value: "RAV" },
        { value: "S1FA" },
        { label: "SBP (SQUAMOSA promoter-binding protein)", value: "SBP" },
        { label: "SRS (Shi-related sequence)", value: "SRS)" },
        { value: "STAT" },
        { label: "TALE (three-amino-acid-loop-extension)", value: "TALE" },
        {
          label: "TCP (Teosinte branched 1/Cycloidea/Proliferating cell)",
          value: "TCP",
        }, // factor
        { label: "tify (TIF[F/Y]XG)", value: "tify" },
        { label: "Trihelix (helix-loop-helix-loop-helix)", value: "Trihelix" },
        { label: "WHY (Whirly)", value: "WHY" },
        { label: "WOX (WUSCHEL-related homeobox)", value: "WOX" },
        { value: "WRKY" },
        { value: "YABBY" },
        { label: "zf-C2H2 (C2H2-type zinc finger)", value: "zf-C2H2" },
        {
          label: "zf-CCCH (CCCH-type zinc finger protein)",
          value: "zf-CCCH",
        },
        {
          label: "zf-Dof (DNA binding with one finger)",
          value: "zf-Dof",
        },
        { label: "ZF-HD (Zinc finger homeodomain)", value: "ZF-HD" },
        { label: "------------------gene family------------------" },
        { label: "AAO (Ascorbic acid oxidase)", value: "AAO" },
        { label: "ABC (ATP-binding cassette)", value: "ABC" },
        { label: "AIG (avrRpt2-induced gene)", value: "AIG" },
        { label: "Alba (acetylation lowers binding affinity)", value: "Alba" },
        { label: "Amts (Ammonium transporter)", value: "Amts" },
        { label: "Ank (ankyrin)", value: "Ank" },
        { label: "ASR (ABA,stress,and ripening-induced)", value: "ASR" },
        { value: "AUX_IAA" },
        { label: "BSP (basic secretory protein)", value: "BSP" },
        { label: "bZIP (basic leucine zipper)", value: "bZIP" },
        { label: "Chs (chitin synthase)", value: "Chs" },
        {
          label: "CIPKs (Calcineurin B-like protein-interacting)",
          value: "CIPKs",
        }, //protein kinases
        { label: "CK (Choline kinase)", value: "CK" },
        { label: "CNGC (cyclic nucleotide-gated ion channel)", value: "CNGC" },
        { label: "COL1 (CONSTANS-LIKE)", value: "COL1" },
        { label: "Csl (cellulose synthase-like)", value: "Csl" },
        {
          label: "DREB (dehydration responsive element-binding)",
          value: "DREB)",
        },
        { label: "AIG", value: "DUF (Domain of unknown function)" },
        { value: "Expansin" },
        { label: "F-box (F-box motifs)", value: "F-box" },
        { label: "FAD2 (FA_desaturase)", value: "FAD2" },
        { label: "FBA (Fructose-1,6-bisphosphate Aldolase)", value: "FBA" },
        { label: "GAox (gibberellin-dioxygenases)", value: "GAox" },
        {
          label: "GASA (Gibberellic Acid Stimulated in Arabidopsis)",
          value: "GASA",
        },
        { label: "GELP (GDSL-type esterases_lipases)", value: "GELP" },
        { label: "HAC (Histone acetylation protein)", value: "HAC" },
        { label: "HAF (TATA box-binding protein binding)", value: "HAF" },
        { label: "HAG (Gcn5-related N- acetyltransferase)", value: "HAG" },
        { label: "HAK (K+ potassium transporter)", value: "HAK" },
        { label: "HDA (Histone deacetylase)", value: "HDA" },
        { label: "HDMA (SWIRM domain)", value: "HDMA" },
        { label: "HMA (heavy metal-associated)", value: "HMA" },
        { label: "HSP (Heat shock proteins)", value: "HSP" },
        { label: "HXK (Hexokinase)", value: "HXK" },
        { label: "H_PPase (H+-PPase)", value: "H_PPase" },
        {
          label: "JHDM (JmjC domain-containing histone demethylase)",
          value: "JHDM",
        },
        { label: "JMJs (JmjC domain_hydroxylase)", value: "JMJs" },
        { label: "LEA (Late embryogenesis abundant)", value: "LEA" },
        { label: "LecRLKs (Lectin receptor-like kinases)", value: "LecRLKs" },
        { label: "LOX (lipoxygenase)", value: "LOX" },
        { label: "LPP (phosphatase superfamily)", value: "LPP" },
        { label: "LRR (Leucine Rich Repeat)", value: "LRR" },
        { label: "LTP (lipid transfer proteins)", value: "LTP" },
        { label: "LysM (lysin motif)", value: "LysM" },
        { label: "MAPKs (Mitogen-activated protein kinase)", value: "MAPKs" },
        {
          label: "MATE (Multidrug and Toxic Compound Extrusion)",
          value: "MATE",
        },
        { value: "MOZ_SAS" },
        { label: "MRP (multidrug resistance proteins)", value: "MRP" },
        { label: "MST (Monosaccharide transporter)", value: "MST" },
        { label: "NBS (nucleotide-binding site)", value: "NBS" },
        {
          label: "NRAMP (natural resistance associated macrophage protein)",
          value: "NRAMP",
        },
        { label: "P-ATPase (P-type H+-ATPase)", value: "P-ATPase" },
        { label: "p450 (Cytochromes P450)", value: "p450" },
        { label: "PAL (Phenylalanine ammonia-lyase)", value: "PAL" },
        {
          label: "PEBP (phosphatidy ethanolamine-binding protein)",
          value: "PEBP",
        },
        { label: "PLD (Phospholipase D)", value: "PLD" },
        { label: "PP2C (phosphatase 2C)", value: "PP2C" },
        { label: "PRMTs (PRMT5 arginine-N-methyltransferase)", value: "PRMTs" },
        { label: "PRO (Probable reticuline oxidase)", value: "PRO" },
        { label: "Prxs (Peroxidases)", value: "Prxs" },
        { label: "PSY (Phytoene synthase)", value: "PSY" },
        { label: "PT (phosphate transporter)", value: "PT" },
        { label: "PYRPYL (pyrabactin resistance)", value: "PYRPYL" },
        { label: "rboh (respiratory burst oxidase homolog)", value: "rboh" },
        { label: "RGP (eversible glycosylation polypeptide)", value: "RGP" },
        { label: "SET (SET domain)", value: "SET" },
        { label: "SOD (Superoxide Dismutase)", value: "SOD" },
        { label: "sox (high mobility group)", value: "sox" },
        { label: "SPL (squamosa promoter-binding protein-like)", value: "SPL" },
        { label: "SRTs (Sir2 family)", value: "SRTs" },
        { label: "TGF (transforming growth factor)", value: "TGF" },
        { label: "TPS (trehalose-6-phosphate synthase)", value: "TPS" },
        { label: "TSs (Terpene synthases)", value: "TSs" },
        { value: "AP2ERF" },
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
    validateFileOrInput1() {
      const upload = this.formState["upload1"];
      const igs = this.formState["gene_sequence1"];
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
    onFinish(values) {
      console.log("Success:", values);
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
    showDomain(values) {
      let body = { ...values };
      // if (body["email"] === undefined || body["email"] == "") {
      //   return;
      // }
      console.log("showDomain onFinish:", body);

      // 校验输入或者文件上传
      const validateRes = this.validateFileOrInput1();
      if (!validateRes) {
        (this.loading_a1 = false), (this.loading_a2 = false);
        this.$message.error(
          "You should either upload a sequence file or directly input sequence string!"
        );
        return;
      }

      // body["tag"] = this.file_tag;
      if (
        this.formState.gene_sequence1 &&
        this.formState.gene_sequence1.trim() != ""
      ) {
        body["tag"] = md5(this.formState.gene_sequence1);
      } else {
        body["tag"] = this.file_tag;
      }
      delete body["upload"];
      this.loading_a2 = true;
      this.$axios
        .post("/api/gene_families", body)
        .then((res) => {
          console.log("res:", res);
          this.showConfirm(res.data.url);
          this.formState = {};
        })
        .catch((error) => {
          this.loading_a2 = false;
          var rsp = error.response;
          console.log("err data :", rsp.data);
          Modal.error({
            title: "Oops!",
            content: rsp.data.error,
          });
        })
        .finally(() => {
          this.loading_a2 = false;
        });
    },
    showSingle(values) {
      let body = { ...values };
      // if (body["email"] === undefined || body["email"] == "") {
      //   return;
      // }
      console.log("showSingle onFinish:", body);
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
      delete body["upload"];
      this.loading_a1 = true;
      this.$axios
        .post("/api/gene_families", body)
        .then((res) => {
          console.log("res:", res);
          this.showConfirm(res.data.url);
        })
        .catch((error) => {
          this.loading_a1 = false;
          var rsp = error.response;
          console.log("err data :", rsp.data);
          Modal.error({
            title: "Oops!",
            content: rsp.data.error,
          });
        })
        .finally(() => {
          this.loading_a1 = false;
          this.formState = {};
        });
    },
    fillExampleGeneSequence() {
      this.formState.gene_sequence = example_gene_sequence;
    },
    fillExampleGeneSequence1() {
      this.formState.gene_sequence1 = example_gene_sequence;
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
</style>
