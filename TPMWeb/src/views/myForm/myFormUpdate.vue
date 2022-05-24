<template>
  <el-card v-loading="loading">
    <el-button type="primary" size="mini" @click="$router.go(-1)"
      >返回</el-button
    >
    <el-form
      ref="form"
      :model="params"
      label-width="auto"
      size="mini"
      :rules="rules"
    >
      <el-form-item label="编号" class="input-name" prop="title"  v-show="type === 'edit'">
        <div>{{ params.form_id }}</div>
      </el-form-item>
      <el-form-item label="标题" class="input-name" prop="title">
        <el-input
          v-model="params.title"
          maxlength="20"
          show-word-limit
          placeholder="请输入标题"
          style="width:60%"
        ></el-input>
      </el-form-item>
      <el-form-item label="表单类型" prop="form_type">
        <el-radio-group v-model="params.form_type" :disabled="type === 'edit'">
          <el-radio v-for="(item, index) in form_type_list" :key="index" :label="item.type_id" >
            {{ item.type_name }}
          </el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="表单状态" prop="form_state">
        <el-radio-group v-model="params.form_state" :disabled="type === 'add'">
          <el-radio v-for="(item, index) in form_state_list" :key="index" :label="item.state_id" >
            {{ item.state_name }}
          </el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="所属应用" prop="produce_id">
        <el-select v-model="params.produce_id" filterable clearable>
          <el-option v-for="item in produces" :key="item.id" :label="item.title" :value="item.id"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="所属项目组" prop="group_id">
        <el-select v-model="params.group_id" filterable clearable>
          <el-option v-for="item in groups" :key="item.id" :label="item.title" :value="item.id"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="指派给" prop="current_user_id">
        <el-select v-model="params.current_user_id" filterable clearable>
          <el-option v-for="item in allUsers" :key="item.id" :label="item.name" :value="item.id"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="负责策划" prop="producer_id">
        <el-select v-model="params.producer_id" filterable clearable>
          <el-option v-for="item in allUsers" :key="item.id" :label="item.name" :value="item.id"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="负责开发" prop="developer_id">
        <el-select v-model="params.producer_id" filterable clearable>
          <el-option v-for="item in allUsers" :key="item.id" :label="item.name" :value="item.id"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="负责测试" prop="tester_id">
        <el-select v-model="params.producer_id" filterable clearable>
          <el-option v-for="item in allUsers" :key="item.id" :label="item.name" :value="item.id"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="上线版本" prop="online_version">
        <el-select v-model="params.online_version" filterable clearable>
          <el-option v-for="item in all_versions" :key="item.id" :label="item.value" :value="item.id"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="内容" class="input-text" prop="remark">
        <el-input
          v-model="params.text"
          type="textarea"
          maxlength="500"
          placeholder="请输入内容"
          show-word-limit
          :rows="10"
        ></el-input>
      </el-form-item>
      <el-form-item>
        <el-button  @click="onSubmit" >{{ type === 'add' ? '立即创建' : '立即修改' }}</el-button>
        <el-button @click="$router.go(-1)">取消</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script>
import { apiFormAdd,apiFormDetail } from '@/api/myForm'
import store from '@/store'

export default {
  name: 'MyFormAdd',
  data() {
    return{
      op_user: store.getters.name,
      params: {
        form_id: this.$route.query.formId,
        form_type: '',
        form_state: 0,
        produce_id: '',
        group_id: undefined,
        current_user: undefined,
        title: '',
        created_user: undefined,
        producer: undefined,
        developer: undefined,
        tester: undefined,
        online_version: '',
      },
      form_state_list: [
        {
          state_id: 0,
          state_name: '待开发'
        },
        {
          state_id: 1,
          state_name: '开发中'
        },
        {
          state_id: 2,
          state_name: '测试中'
        },
        {
          state_id: 3,
          state_name: '已完成'
        },
        {
          state_id: 4,
          state_name: '已删除'
        },
      ],
      form_type_list: [
        {
          type_id: 0,
          type_name: 'BUG单'
        },
        {
          type_id: 1,
          type_name: '需求单'
        },
      ],
      type: this.$route.query.type,
      produces: [],
      groups: [],
      allUsers: [],
      all_versions: []
    }
  },
  created() {
    console.log(this.$route.query.formId)
    if (this.type === 'edit') {
      // 查询form详情
      apiFormDetail({formId: this.$route.query.formId}).then(res =>{
        this.params.form_type = res.data.form_type
      })
    } else {
      // 不查询
    }
  },
  methods: {
    onSubmit() {
      apiFormAdd(this.params).then(res =>{
        //提交之后跳转回列表页
        this.$router.push({
          path: 'MyForm',
        })
      })
    }
  },
}
</script>

<style lang="scss" scoped>
.input-text {
  .el-textarea {
    width: 70%;
  }
}
</style>