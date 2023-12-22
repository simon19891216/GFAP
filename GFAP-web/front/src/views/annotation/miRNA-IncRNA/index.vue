<template>
  <div class="miRNA-IncRNA-container">
    <a-form
      :layout="layout"
      :model="formState"
      v-bind="formItemLayout"
      @finish="onFinish"
      name="time_related_controls"
      @finishFailed="onFinishFailed"
      :rules="rules"
      style="height: 90vh; overflow: scroll"
    >
      <a-form-item name="upload" label="">
        <!-- <a-textarea
          v-model:value="formState['gene_sequence']"
          placeholder="input your sequence file"
          style="width: 50vw"
          :rows="1"
        /> -->
        <label style="color: red">* </label>
        <label>input your sequence file</label>
        <a-upload-dragger
          v-model:file-list="formState['upload']"
          name="file"
          :max-count="1"
          :action="uploadAction"
          :before-upload="beforeUpload"
          :headers="uploadHeaders"
          @change="handleChange"
        >
          <!-- <p class="ant-upload-drag-icon">
            <inbox-outlined></inbox-outlined>
          </p> -->
          <p class="ant-upload-text">
            Click or drag file to this area to upload
          </p>
          <!-- <p class="ant-upload-hint">
            Support for a single upload. The size of file must smaller than 1MB!
          </p> -->
        </a-upload-dragger>
      </a-form-item>
      <div>or</div>
      <a-form-item name="gene_sequence">
        <a-textarea
          v-model:value="formState['gene_sequence']"
          placeholder="directly input gene sequences (fasta format, gene number<=10)"
          style="height: 8vh"
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
      <a-form-item name="input_type" label="input type">
        <!-- <span class="demonstration"></span> -->
        <a-radio-group v-model:value="formState['input_type']">
          <a-radio :value="'miRNA'">miRNA</a-radio>
          <a-radio :value="'lncRNA'">IncRNA</a-radio>
        </a-radio-group>
      </a-form-item>
      <a-form-item name="evalue">
        <a-input
          style="width: 100%"
          v-model:value="formState['evalue']"
          addon-before="E-value"
          placeholder="the default value: 1e-5"
        />
      </a-form-item>
      <a-form-item name="email">
        <a-input
          style="width: 100%"
          v-model:value="formState['email']"
          placeholder="input an email for receiving result (optional)"
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
          annotate
        </a-button>
      </a-form-item>
      <a-form-item> <br /> </a-form-item>
      <a-form-item style="width: 50vw" v-if="output != null">
        <div>{{ output }}</div>
      </a-form-item>
    </a-form>
  </div>
</template>
<script>
import { example_gene_sequence } from "../../../static/sequence_file.ts";
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
        upload: [],
        input_type: "",
        evalue: "",
        species: "",
      },
      // 校验规则
      rules: {
        species: [
          {
            type: "string",
            required: true,
            message: "Please select someOne!",
          },
        ],
        input_type: [
          {
            type: "string",
            required: true,
            message: "Please select annotation type!",
          },
        ],
        // upload: {
        //   type: "array",
        //   required: true,
        //   message: "Please select file!",
        // },
        save: {
          type: "array",
          required: true,
          message: "Please select file!",
        },
        sequence_type: {
          type: "any",
          required: true,
          message: "Please select sequence type!",
        },
        annotation_type: {
          type: "any",
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
      file_tag: null,
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
      this.loading = true;
      this.$axios
        .post("/api/miRNA_lncRNA", body)
        .then((res) => {
          console.log("res:", res);
          // this.$message.success("submission successful");
          this.showConfirm(res.data.url);
        })
        .catch((error) => {
          this.loadin = false;
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
      // // this.file_tag = file.uid;
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
</style>
