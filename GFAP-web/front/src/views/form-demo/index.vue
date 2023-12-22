<template>
  <div class="annotation-container">
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
      <a-form-item name="gene_sequence" label="Gene Sequence">
        <a-textarea
          v-model:value="formState['gene_sequence']"
          placeholder="directly input the gene sequence"
          style="width: 50vw"
          :rows="2"
        />
      </a-form-item>
      <a-form-item> Or </a-form-item>
      <a-form-item name="upload" label="Upload your sequence file">
        <a-upload
          v-model:file-list="formState['upload']"
          name="file"
          :max-count="1"
          :action="uploadAction"
          :headers="uploadHeaders"
          @change="handleChange"
        >
          <a-button>
            <upload-outlined></upload-outlined>
            Click to Upload
          </a-button>
        </a-upload>
      </a-form-item>
      <a-form-item name="sequence_type" label="sequence type(Mandatory)">
        <a-radio-group v-model:value="formState['sequence_type']">
          <a-radio :value="1">protein</a-radio>
          <a-radio :value="2">CDS (coding sequences)</a-radio>
        </a-radio-group>
      </a-form-item>
      <a-form-item name="annotation_type" label="annotation type(Mandatory)">
        <a-checkbox-group v-model:value="formState['annotation_type']">
          <a-checkbox value="GO">GO</a-checkbox>
          <a-checkbox value="KEGG">KEGG</a-checkbox>
          <a-checkbox value="protein domains">protein domains</a-checkbox>
        </a-checkbox-group>
      </a-form-item>
      <a-form-item>
        <a-input
          style="width: 50vw"
          v-model:value="formState['evalue']"
          addon-before="E-value<="
        />
      </a-form-item>
      <a-form-item>
        <a-input
          style="width: 50vw"
          v-model:value="formState['match_percentage']"
          addon-before="match-percentage>="
        />
      </a-form-item>
      <a-form-item>
        <a-select
          v-model:value="value"
          mode="species"
          style="width: 50vw"
          placeholder="select closely related species"
          :options="species_options"
          @change="handleChange"
        >
        </a-select>
      </a-form-item>
      <a-form-item
        :wrapper-col="{
          xs: { span: 16, offset: 0 },
          sm: { span: 16, offset: 8 },
        }"
      >
        <a-button
          type="primary"
          html-type="submit"
          :loading="loading"
          style="width: 100%"
          >Annotation</a-button
        >
      </a-form-item>
      <a-form-item> <br /> </a-form-item>
    </a-form>
  </div>
</template>
<script>
export default {
  name: "form-demo",
  data() {
    return {
      // 表单数据 v-model
      formState: {
        sequence_type: "qn",
        gene_sequence: "",
        evalue: "",
        match_percentage: "",
        species: "",
        upload: [],
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
        upload: {
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
      },
      // 上传文件地址及请求头
      uploadHeaders: {
        authorization: "authorization-text",
      },
      layout: "vertical",
      formItemLayout: {},
      loading: false,
      species_options: [
        { value: "Zea_mays(Poaceae)" },
        { value: "Zingiber_officinale(Zingiberaceae)" },
        { value: "Ziziphus_jujuba(Rhamnaceae)" },
        { value: "Zostera_marina(Zosteraceae)" },
      ],
    };
  },
  computed: {
    uploadAction() {
      if (this.formState["upload"].length == 0) {
        console.log("empty");
        return "http://localhost:10001/api/upload";
      }
      console.log("uploadAction");
      return (
        "http://localhost:10001/api/upload?tag=" +
        this.formState["upload"][0].uid
      );
    },
  },
  methods: {
    onFinish(values) {
      console.log("onFinish:", values);
      this.loading = true;
      this.$axios
        .post("/api/annotation", values)
        .then(() => {
          this.$message.success("submission successful");
        })
        .finally(() => {
          this.loading = false;
          this.formState = {};
        });
    },
    onFinishFailed(err) {
      console.log("Failed:", err);
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
