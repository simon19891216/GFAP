<template>
  <div class="go-kegg-pfam-container">
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
        <label>input your sequence file (fasta format)</label>
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
          <p class="ant-upload-hint">
            Support for a single upload. The size of file must smaller than 1MB!
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
      <a-form-item name="sequence_type" label="sequence type">
        <a-radio-group
          v-model:value="formState['sequence_type']"
          :options="sequence_type_options"
        >
        </a-radio-group>
      </a-form-item>
      <a-form-item name="annotation_type" label="annotation type">
        <a-checkbox-group
          v-model:value="formState['annotation_type']"
          :options="annotation_type_options"
          style="border: 0px solid rgb(225, 0, 0)"
        >
        </a-checkbox-group>
      </a-form-item>
      <a-form-item name="only_ID" label="other output types(optional)">
        <a-checkbox-group
          v-model:value="formState['only_ID']"
          :options="onlyID_options"
        >
        </a-checkbox-group>
      </a-form-item>
      <a-form-item name="evalue">
        <a-input
          style="width: 100%"
          v-model:value="formState['evalue']"
          placeholder="the default value is 1e-5"
          addon-before="E-value<="
        />
      </a-form-item>
      <a-form-item name="match_percentage">
        <a-input
          style="width: 100%"
          v-model:value="formState['match_percentage']"
          placeholder="the default value is 80"
          addon-before="match-percentage>="
        />
      </a-form-item>
      <a-form-item name="alignment_mode" label="select alignment mode">
        <a-select
          v-model:value="formState['alignment_mode']"
          style="width: 100%"
          :options="alignment_mode_options"
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
      <a-form-item
        name="species"
        label="1-annotation with the information of closely related species"
      >
        <a-select
          v-model:value="formState['species']"
          style="width: 100%"
          placeholder="select closely related species"
          :options="species_options"
          @change="handleChange"
        >
        </a-select>
      </a-form-item>
      <a-form-item>
        <a-button
          type="primary"
          html-type="submit"
          :loading="loading_a1"
          style="width: 100%"
          @click="annotate1"
        >
          annotate
        </a-button>
      </a-form-item>

      <a-form-item name="database" label="2-annotation with database">
        <a-select
          v-model:value="formState['database']"
          style="width: 100%"
          placeholder="select a database for annotating protein or CDS seqs"
          :options="database_options"
          @change="handleChange"
        >
        </a-select>
      </a-form-item>
      <a-form-item>
        <a-button
          type="primary"
          html-type="submit"
          :loading="loading_a2"
          style="width: 100%"
          @click="annotate2"
        >
          annotate
        </a-button>
      </a-form-item>
      <br />
      <pre v-if="output != null"> {{ output }} </pre>
    </a-form>
  </div>
</template>
<script>
import { example_gene_sequence } from "../../../static/example_data.ts";
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
        only_ID: [],
        alignment_mode: "",
        species: "",
        database: "",
        email: "",
        upload: [],
      },
      // 校验规则
      rules: {
        sequence_type: {
          type: "string",
          required: true,
          message: "Please select sequence type!",
        },
      },
      layout: "vertical",
      formItemLayout: {},
      loading_data: false,
      loading_a1: false,
      loading_a2: false,
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
      onlyID_options: [{ label: "only GO/KEGG IDs", value: "-only_ID" }],
      alignment_mode_options: [{ value: "fast" }, { value: "sensitive" }],
      database_options: [
        {
          label: "plant-special database",
          value: "psd",
        },
        { label: "complete database", value: "td" },
        { label: "nr", value: "nr" },
        { label: "swissprot", value: "swissprot" },
      ],
      species_options,
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
    validateAnnotationType() {
      const annotation_type = this.formState["annotation_type"];
      const species = this.formState["species"];
      const database = this.formState["database"];
      if (this.loading_a1 == true) {
        if (!annotation_type || annotation_type.length === 0) {
          this.$message.error("Please select anntation type");
          return false;
        }
        if (species == "") {
          this.$message.error("Please select closely related species");
          return false;
        }
      } else if (this.loading_a2 == true) {
        const database = this.formState["database"];
        console.log(database);
        // if (!database || database.length === 0) {
        //   return true;
        // }
        if (database == "") {
          this.$message.error("Please select database type");
          return false;
        }
        if (database === "td" || database === "psd") {
          if (!annotation_type || annotation_type.length === 0) {
            this.$message.error("Please select anntation type");
            return false;
          }
        }
      }
      return true;
    },
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
      // 有上传文件
      if (
        this.formState.gene_sequence &&
        this.formState.gene_sequence.trim() != ""
      ) {
        body["tag"] = md5(this.formState.gene_sequence);
      } else {
        body["tag"] = this.file_tag;
      }
      delete body["upload"];

      if (this.validateAnnotationType() == false) {
        (this.loading_a1 = false), (this.loading_a2 = false);
        // this.$message.error(
        //   "Please select a database for annotating protein or CDS seqs"
        // );
        return;
      }
      // this.loading = true;
      this.$axios
        .post("/api/go_kegg_pfam", body)
        //then 要放在第一个写
        .then((res) => {
          console.log("res:", res);
          if (res == undefined) {
            return;
          }
          this.showConfirm(res.data.url);
          // 提交成功再清除表单内容
          this.formState = {};
        })
        //catch 要放在第二个写
        .catch((error) => {
          var rsp = error.response;
          console.log("err data :", rsp.data);
          Modal.error({
            title: "Oops!",
            content: rsp.data.error,
          });
        })
        //finally 要放在第三个写
        .finally(() => {
          // 取消加载标识
          (this.loading_a1 = false), (this.loading_a2 = false);
        });
    },
    onFinishFailed(err) {
      (this.loading_a1 = false), (this.loading_a2 = false);
      console.log("Failed:", err.error);
    },
    beforeUpload(file) {
      console.log("beforeUpload:", file);
      const isLt1M = file.size / 1024 / 1024 < 1;
      if (!isLt1M) {
        this.$message.error(`file must smaller than 1MB!`);
      }
      // this.file_tag = file.uid;
      this.file_tag = md5(file.uid);
      return isLt1M;
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
    annotate1() {
      this.formState.database = "";
      this.loading_a1 = true;
      // data.database = "";
    },
    annotate2() {
      this.formState.species = "";
      this.loading_a2 = true;
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
