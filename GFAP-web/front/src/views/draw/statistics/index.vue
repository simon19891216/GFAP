<template>
  <div class="statistics-container">
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
          placeholder="If you want to use the example data, the following parameters should be set as: GO draw type: bar_chart"
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
          placeholder="the default value is 10"
          addon-before="cut value<="
        />
      </a-form-item>
      <a-form-item name="annotation_type" label="annotation type">
        <a-radio-group
          v-model:value="formState['annotation_type']"
          :options="annotation_type_options"
          style="border: 0px solid rgb(225, 0, 0)"
        >
        </a-radio-group>
      </a-form-item>
      <a-form-item name="draw_type" label="select draw type">
        <a-select
          v-model:value="formState['draw_type']"
          style="width: 100%"
          placeholder="select draw type"
          :options="drawtype_options"
          @change="handleChange"
        >
        </a-select>
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
      <a-form-item
        name="color"
        label="click below to select your favorite color"
      >
        <input
          type="color"
          v-model="formState['color']"
          style="margin-left: 0.25rem"
        />
      </a-form-item>
      <div>or</div>
      <a-form-item name="singlecolor" label="">
        <a-checkbox-group
          v-model:value="formState['singlecolor']"
          :options="singlecolor_options"
          style="margin-left: 0.8rem"
        >
        </a-checkbox-group>
      </a-form-item>
      <!-- <a-form-item name="save_type" label="select save type">
        <a-select
          v-model:value="formState['save_type']"
          style="width: 100%"
          placeholder="select save type"
          :options="savetype_options"
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
        evalue: null,
        cut_value: null,
        gene_number: null,
        species: "",
        color: "",
        colormodel: "",
        draw_type: "",
        singlecolor: [],
        database: "",
        save_type: "",
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
        draw_type: [
          {
            type: "string",
            required: true,
            message: "Please select draw type",
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
        annotation_type: {
          type: "string",
          required: true,
          message: "Please select annotation type!",
        },
        // save_type: [
        //   {
        //     type: "string",
        //     required: true,
        //     message: "Please select save type!",
        //   },
        // ],
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
      savetype_options: [
        {
          value: "svg",
        },
        {
          value: "pdf",
        },
      ],
      drawtype_options: [{ value: "bar_chart" }, { value: "heatmap" }],
      annotation_type_options: [
        { label: "GO", value: "-go" },
        { label: "KEGG", value: "-kegg" },
        { label: "protein domains", value: "-pfam" },
      ],
      singlecolor_options: [
        { label: "using single_color", value: "-singlecolor" },
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
      this.loading = true;
      this.$axios
        .post("/api/statistics", body)
        .then((res) => {
          console.log("res:", res);
          if (res.data.command.endsWith(".svg")) {
            this.result_image = res.data.output;
          }
          this.showConfirm(res.data.url);
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
          this.formState = {};
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

.ant-form-item {
  margin: 0 0 12px;
}
</style>
