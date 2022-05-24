<template>
  <div class="app-container">

    <!--对话框嵌套表，使用el-dialog-->
    <el-dialog :title="dialogProductStatus==='ADD'?'添加产品':'修改产品'" :visible.sync="dialogProductShow">
      <el-form :model="product">
        <el-form-item v-if="dialogProductStatus==='UPDATE'" label="编号" label-width="100px">
          <el-input v-model="product.id" style="width: 80%" disabled />
        </el-form-item>
        <el-form-item label="名称" label-width="100px">
          <el-input v-model="product.title" placeholder="请填写中文名称" style="width: 80%" />
        </el-form-item>
        <el-form-item label="唯一码" label-width="100px">
          <el-input v-model="product.keyCode" placeholder="产品/项目唯一码" style="width: 80%" />
        </el-form-item>
        <el-form-item label="备注" label-width="100px">
          <el-input v-model="product.desc" type="textarea" placeholder="备注说明" style="width: 80%" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogProductShow = false">取 消</el-button>
        <el-button v-if="dialogProductStatus==='ADD'" type="primary" @click="pCreate()">添 加</el-button>
        <el-button v-if="dialogProductStatus==='UPDATE'" type="primary" @click="pUpdate()">编 辑</el-button>
      </span>
    </el-dialog>

    <div class="filter-container">
      <el-button type="primary" icon="el-icon-plus" style="float:right" @click="dialogProduct()">新增</el-button>
    </div>
    <div class="filter-container">
      <el-form :inline="true">
        <el-form-item label="keycode">
          <el-input v-model="params.keyCode" placeholder="keycode" style="width: 200px;" clearable />
        </el-form-item>
        <el-form-item label="title">
          <el-input v-model="params.title" placeholder="输入title" style="width: 200px;" clearable />
        </el-form-item>
        <el-form-item label="desc">
          <el-input v-model="params.desc" placeholder="输入desc" style="width: 200px;" clearable />
        </el-form-item>
        <el-button @click="selectBotton">查询</el-button>
        <el-button @click="clearSearch">重置</el-button>
      </el-form>
    </div>
    <el-table :data="tableData">
      <el-table-column prop="id" label="编号" />
      <el-table-column prop="title" label="名称" />
      <el-table-column prop="keyCode" label="代号" />
      <el-table-column prop="desc" label="描述" show-overflow-tooltip />
      <el-table-column prop="operator" label="操作人" />
      <el-table-column :formatter="formatDate" prop="update" label="操作时间" />
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-link icon="el-icon-edit" @click="dialogProductUpdate(scope.row)">编辑</el-link>
          <el-link icon="el-icon-delete" @click="pDelete(scope.row)">删除</el-link>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      :page-sizes="[10, 20, 30, 40]"
      :page-size="10"
      :current-page.sync="params.page"
      layout="total, sizes, prev, pager, next, jumper"
      :total="params.total"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange">
    </el-pagination>
  </div>
</template>

<script>
// 引用src/api/proudct 配置的请求列表方法
import { apiProductList, apiProductCreate, apiProductUpdate, apiProductDelete } from '@/api/product'
import store from '@/store'
import moment from 'moment'

export default {
  name: 'Product', // 页面名称
  // data() 数据\属性，固定return中配置
  data() {
    return {
      tableData: [],
      op_user: store.getters.name,
      product: {
        id: undefined,
        title: undefined,
        keyCode: undefined,
        desc: undefined,
        operator: this.op_user
      },
      dialogProductShow: false,
      dialogProductStatus: 'ADD',
      params: {
        title: '',
        keyCode: '',
        desc: '',
        page: 1,
        size: 10,
        total: 0
      }
    }
  },
  // 页面生命周期中的创建阶段调用
  created() {
    // 调用methods的方法，即初次加载就请求数据
    this.getProductList()
  },
  methods: {
    getProductList() {
      apiProductList(this.params).then(response => {
        this.tableData = response.data
        console.log(response.total)
        this.params.total = response.total
      })
    },

    selectBotton() {
      this.params.page = 1
      this.getProductList()
    },

    clearSearch() {
      this.params.title = ''
      this.params.keyCode = ''
      this.params.desc = ''
    },

    formatDate(row, column) {
      const date = row[column.property]
      if (date === undefined) {
        return ''
      }
      return moment(date).utcOffset(0).format('YYYY-MM-DD HH:mm')
    },

    dialogProduct() {
      // 添加先初始化空状态
      this.product.id = undefined
      this.product.keyCode = ''
      this.product.title = ''
      this.product.desc = ''
      this.product.operator = this.op_user

      // 弹出对话框设置为true
      this.dialogProductShow = true
    },

    pCreate() {
      // 请求API进行添加
      apiProductCreate(this.product).then(response => {
        // 如果request.js没有拦截即表示成功，给出对应提示和操作
        this.$notify({
          title: '成功',
          message: '项目或产品添加成功',
          type: 'success'
        })
        // 关闭对话框
        this.dialogProductShow = false
        // 重新查询刷新数据显示
        this.getProductList()
      })
    },

    dialogProductUpdate(row) {
      this.product.id = row.id
      this.product.keyCode = row.keyCode
      this.product.title = row.title
      this.product.desc = row.desc
      this.product.operator = this.op_user

      this.dialogProductStatus = 'UPDATE'
      this.dialogProductShow = true
      console.log(this.dialogProductStatus)
    },

    pUpdate() {
      apiProductUpdate(this.product).then(response => {
        this.$notify({
          title: '成功',
          message: '项目或产品修改成功',
          type: 'success'
        })
      }).catch(() => {
        this.$notify({
          title: '失败',
          message: '项目或产品修改失败',
          type: 'fail'
        })
      })
      this.dialogProductShow = false
      this.getProductList()
    },

    pDelete(row) {
      this.$confirm('是否确认删除', '提示1', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.product.id = row.id
        this.product.keyCode = row.keyCode
        this.product.title = row.title
        this.product.desc = row.desc
        this.product.operator = this.op_user
        apiProductDelete(this.product).then(response => {
          this.$notify({
            title: '成功',
            message: '项目删除成功',
            type: 'success'
          })
        })
        this.getProductList()
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消删除'
        })
      })
    },

    handleSizeChange(val) {
      this.params.size = val
      this.getProductList()
    },

    handleCurrentChange(val) {
      this.params.page = val
      this.getProductList()
    }
  }
}
</script>

<style scoped>
  .el-pagination {
      text-align: right;
  }
</style>
