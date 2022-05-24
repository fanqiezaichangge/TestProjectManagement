<template>
  <el-card>
    <el-button type="primary" size="mini" @click="$router.go(-1)"
      >返回</el-button
    >
    <ul>
      <li>
        <strong>编号</strong>
        <p>{{ dataTable.form_id }}</p>
      </li>
      <li>
        <strong>标题</strong>
        <p>{{ dataTable.title }}</p>
      </li>
      <li>
        <strong>状态</strong>
        <p>{{ dataTable.formState }}</p>
      </li>
      <li>
        <strong>所属产品</strong>
        <p>{{ dataTable.group_id }}</p>
      </li>
      <li>
        <strong>当前指派</strong>
        <p>{{ dataTable.current_user_name }}</p>
      </li>
      <li>
        <strong>创建人</strong>
        <p>{{ dataTable.created_user_name }}</p>
      </li>
      <li>
        <strong>创建时间</strong>
        <p>{{ createdTime }}</p>
      </li>
      <li>
        <strong>上次修改时间</strong>
        <p>{{ modifiedTime }}</p>
      </li>
      <li>
        <strong>负责产品</strong>
        <p>{{ dataTable.producer_name }}</p>
      </li>
      <li>
        <strong>负责开发</strong>
        <p>{{ dataTable.developer_name }}</p>
      </li>
      <li>
        <strong>负责测试</strong>
        <p>{{ dataTable.tester_name }}</p>
      </li>
      <li>
        <strong>上线版本</strong>
        <p>{{ dataTable.online_version }}</p>
      </li>
      <li>
        <strong>内容</strong>
        <p>{{ dataTable.text }}</p>
      </li>
      <li v-if="dataTable.file_url">
        <strong>图片</strong>
        <div class="img-box">
          <img :src="dataTable.file_url" alt="" />
        </div>
      </li>
    </ul>
  </el-card>
</template>

<script>
import { apiFormDetail } from '@/api/myForm'
import moment from 'moment'

export default {
  name: 'MyFormDetail',
  data() {
    return{
      dataTable: {},
      formId: '',
      // createdTime: undefined,
      // modifiedTime: undefined
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
    }
  },
  created() {
    this.formId = this.$route.query.formId
    this.formDetail()
  },
  computed: {
    createdTime() {
      const date = this.dataTable.created_time
      // console.log(date)
      if (date === undefined) {
        return ''
      }
      return moment(date).utcOffset(0).format('YYYY-MM-DD HH:mm')
    },
    modifiedTime() {
      const date = this.dataTable.modified_time
      if (date === undefined) {
        return ''
      }
      return moment(date).utcOffset(0).format('YYYY-MM-DD HH:mm')
    },
    formState() {
      for (let i = 0; i < this.form_state_list.length; i++) {
        console.log(this.dataTable.form_state)
        if (form_state_list[i].state_id === this.dataTable.form_state) {
          return form_state_list[i].state_name
        }
      }
    },
    formType() {
      for (let i = 0; i < this.form_type_list.length; i++) {
        if (form_type_list[i].type_id === this.dataTable.form_type) {
          return form_type_list[i].type_name
        }
      }
    }
  },
  methods: {
    formDetail() {
      // console.log(this.formId)
      apiFormDetail({formId: Number(this.formId)}).then(res =>{
        this.dataTable = res.data
        // this.createdTime = moment(this.dataTable.created_time).utcOffset(0).format('YYYY-MM-DD HH:mm')
        // this.modifiedTime = moment(this.dataTable.modified_time).utcOffset(0).format('YYYY-MM-DD HH:mm')
      })
    },
  }
}
</script>
  
<style lang="scss" scoped>
ul {
  // list-style: none;
  li {
    display: flex;
    // margin-top: 0px;
    strong {
      display: inline-block;
      margin-right: 20px;
      // width: 120px;
      // text-align: right;
    }
    p {
        margin-top: 0px;
    }
  }
}
</style>