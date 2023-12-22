<template>
  <div class="extraction-container">
    <a-form :layout="layout" style="height: 90vh; overflow: scroll">
      <a-form
        :layout="layout"
        :model="formState"
        style="border: 2px solid rgb(235, 250, 250)"
        v-bind="formItemLayout"
        @finish="doExtraction"
        name="time_related_controls"
        @finishFailed="onFinishFailed"
        :rules="rules"
        :labelCol="{ offset: 0 }"
        :wrapperCol="{ offset: 0 }"
      >
        <h2
          style="
            border: 0px solid rgb(225, 0, 0);
            font-weight: bold;
            color: red;
          "
        >
          Extract Content
        </h2>
        <!-- sub-title="This is a subtitle" -->
        <a-form-item name="ar_upload" label="input your annotation result">
          <a-upload-dragger
            v-model:file-list="formState['ar_upload']"
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
        <a-form-item name="id_upload" label="input ID file">
          <a-upload-dragger
            v-model:file-list="formState['id_upload']"
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
        <a-form-item name="sequence_type" label="ID type">
          <a-radio-group
            v-model:value="formState['sequence_type']"
            :options="sequence_type_options"
          >
          </a-radio-group>
        </a-form-item>
        <a-form-item name="email">
          <a-input
            v-model:value="formState['email']"
            placeholder="input an email for receiving results (optional)"
            addon-before="email"
          />
        </a-form-item>
        <a-form-item>
          <a-button
            type="primary"
            html-type="submit"
            :loading="loading1"
            style="width: 100%"
          >
            extraction
          </a-button>
        </a-form-item>
      </a-form>
      <br />
      <!-- <a-form
        :layout="layout"
        :model="formState"
        v-bind="formItemLayout"
        style="border: 2px solid rgb(235, 250, 250)"
        @finish="doMerge"
        name="time_related_controls"
        label="merge annotation gesuls"
        @finishFailed="onFinishFailed"
        :rules="rules"
        :labelCol="{ offset: 0 }"
        :wrapperCol="{ offset: 0 }"
      >
        <h2
          style="
            border: 0px solid rgb(225, 0, 0);
            font-weight: bold;
            color: red;
          "
        >
          Merge Annotation Results
        </h2>
        <a-form-item name="sf_upload" label="upload your sequence file">
          <a-upload
            v-model:file-list="formState['sf_upload']"
            name="file"
            :max-count="1"
            :action="uploadAction"
            :before-upload="beforeUpload"
            :headers="uploadHeaders"
            @change="handleChange"
          >
            <a-button style="width: 80.5vw">
              <upload-outlined></upload-outlined>
              Upload single file
            </a-button>
          </a-upload>
        </a-form-item>
        <a-form-item
          name="upload"
          label="upload the related annotation results"
        >
          <a-upload-dragger
            v-model:file-list="formState['upload']"
            name="file"
            :multiple="true"
            :action="uploadDirAction"
            :before-upload="beforeDirUpload"
            :headers="uploadHeaders"
            @change="handleChange"
          >
            <p class="ant-upload-text">
              Click or drag file to this area to upload (bulk)
            </p>
          </a-upload-dragger>
        </a-form-item>
        <a-form-item name="email">
          <a-input
            v-model:value="formState['email']"
            placeholder="input an email for receiving results (optional)"
            addon-before="email"
          />
        </a-form-item>
        <a-form-item>
          <a-button
            type="primary"
            html-type="submit"
            :loading="loading2"
            style="width: 100%"
          >
            merge annotation gesuls
          </a-button>
        </a-form-item>
      </a-form> -->
      <br />
      <a-form
        :layout="layout"
        :model="formState"
        v-bind="formItemLayout"
        style="border: 2px solid rgb(235, 250, 250)"
        @finish="ExtractCodingSequences"
        name="time_related_controls"
        @finishFailed="onFinishFailed"
        :rules="rules"
        :labelCol="{ offset: 0 }"
        :wrapperCol="{ offset: 0 }"
      >
        <h2
          style="
            border: 0px solid rgb(225, 0, 0);
            font-weight: bold;
            color: red;
          "
        >
          Extract Coding Sequences from Transcripts
        </h2>
        <a-form-item
          name="code_sequence"
          label="input fasta-format transcripts"
        >
          <a-textarea
            v-model:value="formState['code_sequence']"
            placeholder="input the sequences of transcript (fasta format, this website allows users to input at most ten sequences for analysis, if you want to analyze multiple transcripts, you can use GFAP-linux version)"
            style="height: 15vh"
          >
          </a-textarea>
          <a-button
            type="primary"
            :loading="loading_data"
            style="width: 100%"
            @click="fillExampleCodeSequence"
          >
            using example data
          </a-button>
        </a-form-item>
        <!-- <div>{{ formState["code_sequence"] }}</div> -->
        <a-form-item>
          <a-button
            type="primary"
            html-type="submit"
            :loading="loading3"
            style="width: 100%"
            @click="null"
          >
            extract coding sequence
          </a-button>
        </a-form-item>
      </a-form>
      <br />
      <a-form
        :layout="layout"
        :model="formState"
        v-bind="formItemLayout"
        style="border: 2px solid rgb(235, 250, 250)"
        @finish="BuildRNADatabase"
        name="time_related_controls"
        @finishFailed="onFinishFailed"
        :rules="rules"
        :labelCol="{ offset: 0 }"
        :wrapperCol="{ offset: 0 }"
      >
        <h2
          style="
            border: 0px solid rgb(225, 0, 0);
            font-weight: bold;
            color: red;
          "
        >
          Building sgRNA Database
        </h2>
        <a-form-item name="sg_upload" label="input genomic sequence file">
          <a-upload-dragger
            v-model:file-list="formState['sg_upload']"
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
        <!-- <div>{{ formState["code_sequence"] }}</div> -->
        <a-form-item>
          <a-button
            type="primary"
            html-type="submit"
            :loading="loading4"
            style="width: 100%"
            @click="null"
          >
            build sgRNA database
          </a-button>
        </a-form-item>
      </a-form>
      <a-form-item> <br /> </a-form-item>
      <a-form-item style="width: 50vw" v-if="output != null">
        <a-label> {{ output }} </a-label>
      </a-form-item>
    </a-form>
  </div>
</template>
<script>
import { example_code_sequence } from "../../../static/extraction_code.ts";
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
        code_sequence: "",
        annotation_type: [],
        evalue: null,
        match_percentage: null,
        species: "",
        database: "",
        ar_upload: [],
        id_upload: [],
        sf_upload: [],
        sg_upload: [],
        upload: [],
      },
      // 校验规则
      rules: {
        ar_upload: {
          type: "array",
          required: true,
          message: "Please upload annotation result!",
        },
        id_upload: {
          type: "array",
          required: true,
          message: "Please upload ID file!",
        },
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
          message: "Please select ID type!",
        },
        code_sequence: {
          type: "string",
          required: true,
          message: "Please input the sequences of transcript!",
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
      loading1: false,
      loading2: false,
      loading3: false,
      loading4: false,
      output: null,
      file_tag: null,
      dir_tag: null,
      sequence_type_options: [
        { label: "gene ID", value: "-exgid" },
        { label: "GO/KEGG/Pfam ID", value: "-exfid" },
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
    uploadDirAction() {
      return "/api/uploadDir?dir=" + this.dir_tag + "&tag=" + this.file_tag;
    },
    // 上传文件地址及请求头
    uploadHeaders() {
      return {
        authorization: "authorization-text",
      };
    },
  },
  methods: {
    onFinish(values) {
      let body = { ...values };
      console.log("onFinish:", body);
      // body["tag"] = this.file_tag;
      // delete body["ar_upload"];
      // delete body["id_upload"];
      // delete body["sf_upload"];
      // this.loading = true;
      // this.$axios
      //   .post("/api/extraction", body)
      //   .then((res) => {
      //     console.log("res:", res);
      //           //     this.showConfirm(res.data.url);
      //   })
      //   .finally(() => {
      //     this.loading = false;
      //     this.formState = {};
      //   });
    },
    onFinishFailed(err) {
      console.log("Failed:", err);
    },
    doExtraction(values) {
      let body = { ...values };
      console.log("onFinish:", body);
      body["tag"] = body["ar_upload"][0].uid;
      body["tag1"] = body["id_upload"][0].uid;
      delete body["ar_upload"];
      delete body["id_upload"];
      delete body["sf_upload"];
      this.loading1 = true;
      this.$axios
        .post("/api/extraction", body)
        .then((res) => {
          console.log("res:", res);
          this.showConfirm(res.data.url);
        })
        .catch((error) => {
          this.loading_1 = false;
          var rsp = error.response;
          console.log("err data :", rsp.data);
          this.$message.error(rsp.data.error);
        })
        .finally(() => {
          this.loading1 = false;
          this.formState = {};
        });
    },
    doMerge(values) {
      let body = { ...values };
      console.log("onFinish:", body);
      body["tag"] = body["sf_upload"][0].uid;
      body["dir_tag"] = this.dir_tag;
      delete body["ar_upload"];
      delete body["id_upload"];
      delete body["sf_upload"];
      this.loading2 = true;
      this.$axios
        .post("/api/merge", body)
        .then((res) => {
          console.log("res:", res);
          this.showConfirm(res.data.url);
        })
        .finally(() => {
          this.loading2 = false;
          this.formState = {};
          this.dir_tag = null;
        });
    },
    beforeUpload(file) {
      console.log("beforeUpload:", file);
      this.file_tag = file.uid;
      // this.file_tag = md5(file.uid);
      return true;
      // console.log("beforeUpload:", file);
      // const isLt1M = file.size / 1024 / 1024 < 1;
      // if (!isLt1M) {
      //   this.$message.error(`file must smaller than 1MB!`);
      // }
      // this.file_tag = file.uid;
      // return isLt1M;
    },
    beforeDirUpload(file) {
      console.log("beforeUpload:", file);
      if (this.dir_tag == null) {
        this.dir_tag = file.uid;
      }
      this.file_tag = file.uid;
      return true;
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
    fillExampleCodeSequence() {
      this.formState.code_sequence = example_code_sequence;
    },
    ExtractCodingSequences(values) {
      let body = { ...values };
      console.log("extract:", body);
      body["tag"] = md5(this.formState.code_sequence);

      delete body["upload"];
      const igs = this.formState["code_sequence"];
      // console.log(igs);
      if (igs.trim() === "") {
        this.$message.error(
          "You should either upload a sequence file or directly input sequence string!"
        );
        return;
      }
      this.loading3 = true;
      this.$axios
        .post("/api/extractcode", body)
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
          this.loading3 = false;
          this.formState = {};
        });
    },
    BuildRNADatabase(values) {
      let body = { ...values };
      console.log("onFinish:", body);
      body["tag"] = body["sg_upload"][0].uid;
      delete body["sg_upload"];
      this.loading4 = true;
      this.$axios
        .post("/api/builddatabase", body)
        .then((res) => {
          console.log("res:", res);
          this.showConfirm(res.data.url);
        })
        .catch((error) => {
          this.loading4 = false;
          var rsp = error.response;
          console.log("err data :", rsp.data);
          this.$message.error(rsp.data.error);
        })
        .finally(() => {
          this.loading4 = false;
          this.formState = {};
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
