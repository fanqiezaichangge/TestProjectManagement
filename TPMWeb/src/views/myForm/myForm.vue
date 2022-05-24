<template>
  <div class="app-container">
    <div class="filter-container">
      <el-form :inline="true" :model="params" ref="params">
        <el-form-item label="标题" prop="title">
            <el-input v-model="params.title" placeholder="搜索标题" style="width: 200px;" clearable />
        </el-form-item>
        <el-form-item label="ID" prop="form_id">
            <el-input v-model="params.form_id" placeholder="搜索ID" style="width: 200px;" clearable />
        </el-form-item>
        <el-form-item label="类型" prop="form_type">
            <el-select v-model="params.form_type" filterable clearable>
                <el-option value="" label="所有" ></el-option>
                <el-option v-for="item in form_types" :key="item.id" :label="item.title" :value="item.id"></el-option>
            </el-select>
        </el-form-item>
        <el-form-item label="产品" prop="produce_id">
            <!-- 这里最好是能取到用户所在的部门和产品，自动填入，有必要的话再做个权限控制 -->
            <el-select v-model="params.produce_id" filterable clearable>
                <el-option value="" label="所有" ></el-option>
                <el-option v-for="item in produces" :key="item.id" :label="item.title" :value="item.id"></el-option>
            </el-select>
        </el-form-item>
        <el-form-item label="现指定人">
            <el-input v-model="params.current_user" placeholder="搜索现指定人" style="width: 200px;" clearable />
        </el-form-item>
        <el-form-item label="创建人">
            <el-input v-model="params.created_user" placeholder="搜索创建人" style="width: 200px;" clearable />
        </el-form-item>
        <el-form-item label="负责策划">
            <el-input v-model="params.producer" placeholder="搜索策划" style="width: 200px;" clearable />
        </el-form-item>
        <el-form-item label="负责程序">
            <el-input v-model="params.developer" placeholder="搜索程序" style="width: 200px;" clearable />
        </el-form-item>
        <el-form-item label="负责测试">
            <el-input v-model="params.tester" placeholder="搜索测试" style="width: 200px;" clearable />
        </el-form-item>
        <el-form-item label="上线版本">
            <el-select v-model="params.online_version" filterable clearable>
                <el-option value="" label="所有" ></el-option>
                <el-option v-for="item in all_versions" :key="item.id" :label="item.title" :value="item.id"></el-option>
            </el-select>
        </el-form-item>
        <el-button @click="selectBotton">查询</el-button>
        <el-button @click="clearSearch">重置</el-button>
      </el-form>
    </div>
    <div class="filter-container">
      <el-button type="primary" icon="el-icon-plus" style="float:right" @click="dialogAddForm()">新增</el-button>
    </div>
    <div>
      <el-table :data="tableData">
          <el-table-column prop="form_id" label="id" />
          <el-table-column prop="title" label="标题" v-popover:popoverRef>
            <template slot-scope="scope">
              <el-popover
              placement="left"
              :title="scope.row.title"
              width="200"
              trigger="hover"
              :content="scope.row.text">
              <div slot="reference">{{scope.row.title}}
              </div>
              </el-popover>
            </template>
          </el-table-column>
          <el-table-column prop="form_type" label="类型" />
          <el-table-column prop="form_state" label="状态" />
          <el-table-column prop="current_user_name" label="指派给" />
          <el-table-column prop="created_user_name" label="创建人" />
          <el-table-column prop="online_version" label="上线版本" />
          <el-table-column :formatter="formatDate" prop="modified_time" label="操作时间" />
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-link icon="el-icon-edit" @click="formDetail(scope.row)">详情</el-link>
              <el-link icon="el-icon-edit" @click="formUpdate(scope.row)">编辑</el-link>
            </template>
          </el-table-column>
      </el-table>
      <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :page-sizes="[10, 20, 30, 40]"
          :page-size="10"
          :current-page.sync="params.page"
          layout="total, sizes, prev, pager, next, jumper"
          :total="params.total">
      </el-pagination>
    </div>
  </div>
</template>

<script>
import { apiFormList } from '@/api/myForm'
import moment from 'moment'

export default ({
  name: 'MyForm',
  data() {
    return {
      tableData: [],
      params: {
        form_id: undefined,
        form_type: '',
        form_state: undefined,
        produce_id: '',
        group_id: undefined,
        current_user: undefined,
        title: '',
        created_user: undefined,
        producer: undefined,
        developer: undefined,
        tester: undefined,
        online_version: '',
        page: 1,
        size: 10,
        total: 0
      },
      all_versions: [],
      form_types: [],
      produces: [],
      all_producers: [],
      all_developers: [],
      all_testers: [],
      all_users: [],
      addFormShow: false,
      // popUpShow: false,
      // positionStyle: {top:'0px',left:'20px'}
    }
  },
  created() {
    this.params.page = 1
    this.getFormList()
   },
  methods: {
    selectBotton() {
      this.params.page = 1
      this.getFormList()
    },
    dialogAddForm() {
      this.$router.push({
        name: 'formUpdate',
        query: {
          type: 'add'
        }
      })
    },
    // 不用鼠标事件了，popover组件里直接有hover的事件
    // titleenter() {
    //   this.popUpShow = true
    //   this.$refs.popoverRef.doShow()
    //   console.log('enter')
    // },
    // titleleave() {
    //   this.popUpShow = false
    //   this.$refs.popoverRef.doClose()
    //   console.log('leave')
    // },
    clearSearch() {
      // this.params.form_id = ''
      // this.params.form_type = ''
      // this.params.form_state = ''
      // this.params.produce_id = ''
      // this.params.group_id = ''
      // this.params.current_user = ''
      // this.params.title = ''
      // this.params.created_user = ''
      // this.params.producer = ''
      // this.params.developer = ''
      // this.params.tester = ''
      // this.params.online_version = ''
      // console.log(this.params.title)
      this.$refs.params.resetFields()
      // console.log(this.params.title)
    },
    getFormList() {
      apiFormList(this.params).then(res => {
        this.tableData = res.data
        this.params.total = res.total
      })
    },
    handleSizeChange(val) {
      this.params.size = val
      this.getFormList()
    },

    handleCurrentChange(val) {
      this.params.page = val
      this.getFormList()
    },

    formatDate(row, column) {
      const date = row[column.property]
      if (date === undefined) {
        return ''
      }
      return moment(date).utcOffset(0).format('YYYY-MM-DD HH:mm')
    },

    formDetail(row) {
      this.$router.push({
        path: 'formDetail',
        query: {
          formId: row.form_id
        }
      })
    },

    formUpdate(row) {
      this.$router.push({
        path: 'formUpdate',
        query: {
          type: 'edit',
          formId: row.form_id
        }
      })
    }
  }
})
</script>
