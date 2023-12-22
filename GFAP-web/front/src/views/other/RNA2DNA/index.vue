<template>
  <div class="RNA2DNA-container">
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
        <label>input your RNA-sequence file</label>
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
          placeholder="directly input gene sequences (fasta format, gene number<=10  )"
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
          translate
        </a-button>
      </a-form-item>
      <a-form-item> <br /> </a-form-item>
      <a-form-item style="width: 50vw" v-if="output != null">
        <a-label> {{ output }} </a-label>
      </a-form-item>
    </a-form>
  </div>
</template>
<script>
import { example_gene_sequence } from "../../../static/RNA_sequence_file.ts";
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
        annotation_type: [],
        evalue: null,
        match_percentage: null,
        species: "",
        database: "",
        upload: [],
      },
      // 校验规则
      rules: {
        // upload: {
        //   type: "array",
        //   required: true,
        //   message: "Please select sequence file!",
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
      file_tag: null,
      sequence_type_options: [
        { label: "protein", value: "-qp" },
        { label: "CDS (coding sequences)", value: "-qn" },
      ],
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
      database_options: [
        {
          label: "plant-special database",
          value: "-awd psd",
        },
        { label: "complete database", value: "-awd td" },
        { label: "nr", value: "-awd nr" },
        { label: "swissprot", value: "-awd swissprot" },
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
    onFinish(values) {
      let body = { ...values };
      console.log("onFinish:", body);
      // 校验输入或者文件上传
      const validateRes = this.validateFileOrInput();
      if (!validateRes) {
        this.$message.error(
          "You should either upload a sequence file or directly input sequence string!"
        );
        return;
      }
      if (
        this.formState.gene_sequence &&
        this.formState.gene_sequence.trim() != ""
      ) {
        body["tag"] = md5(this.formState.gene_sequence);
      } else {
        body["tag"] = this.file_tag;
      }
      delete body["upload"];
      this.loading = true;
      this.$axios
        .post("/api/RNA2DNA", body)
        .then((res) => {
          console.log("res:", res);
          this.showConfirm(res.data.url);
        })
        //catch 要放在第二个写
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
          this.formState = {};
        });
    },
    onFinishFailed(err) {
      console.log("Failed:", err);
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

.ant-form-item {
  margin: 0 0 12px;
}
</style>
