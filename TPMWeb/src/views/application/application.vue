<template>
  <div class="app-container">

    <!--对话框嵌套表，使用el-dialog-->
    <!-- <el-dialog :title="dialogAppStatus==='ADD'?'添加产品':'修改产品'" :visible.sync="dialogAppShow">
      <el-form :model="application">
        <el-form-item v-if="dialogAppStatus==='UPDATE'" label="编号" label-width="100px">
          <el-input v-model="application.id" style="width: 80%" disabled />
        </el-form-item>
        <el-form-item label="名称" label-width="100px">
          <el-input v-model="application.title" placeholder="请填写中文名称" style="width: 80%" />
        </el-form-item>
        <el-form-item label="唯一码" label-width="100px">
          <el-input v-model="application.keyCode" placeholder="产品/项目唯一码" style="width: 80%" />
        </el-form-item>
        <el-form-item label="备注" label-width="100px">
          <el-input v-model="application.desc" type="textarea" placeholder="备注说明" style="width: 80%" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogAppStatus = false">取 消</el-button>
        <el-button v-if="dialogAppStatus==='ADD'" type="primary" @click="pCreate()">添 加</el-button>
        <el-button v-if="dialogAppStatus==='UPDATE'" type="primary" @click="pUpdate()">编 辑</el-button>
      </span>
    </el-dialog> -->
    <el-drawer :title="appAction==='ADD'?'添加应用':'修改应用'" :visible.sync="drawerVisiable" direaction="rtl">
      <el-form :model="application" :rules="drawerRules" ref="application" label-width="120px">
        <el-form-item label="应用ID" prop="appId">
          <el-input v-model="application.appId">
          </el-input>
        </el-form-item>
        <el-form-item label="归属分类" prop="productId">
          <el-select v-model="application.productId">
            <el-option
             v-for="item in options"
             :key="item.id"
             :label="item.title"
             :value="item.id"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="APP名称" prop="note">
          <el-input v-model="application.note">
          </el-input>
        </el-form-item>
        <el-form-item label="测试人员" prop="tester">
          <el-input v-model="application.tester">
          </el-input>
        </el-form-item>
        <el-form-item label="开发人员" prop="developer">
          <el-input v-model="application.developer">
          </el-input>
        </el-form-item>
        <el-form-item label="产品" prop="producer">
          <el-input v-model="application.producer">
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button @click="commitApp('application')">添加</el-button>
        </el-form-item>
      </el-form>
    </el-drawer>

    <div class="filter-container">
      <el-button type="primary" icon="el-icon-plus" style="float:right" @click="dialogApplication()">新增</el-button>
    </div>
    <div class="filter-container">
      <el-form :inline="true">
        <el-form-item label="appId">
          <el-input v-model="params.appId" placeholder="appId" style="width: 200px;" clearable />
        </el-form-item>
        <el-form-item label="产品名称">
          <el-select v-model="params.productId" filterable clearable>
            <el-option value="" label="所有"></el-option>
            <el-option v-for="item in options" :key="item.id" :label="item.title" :value="item.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="APP名称">
          <el-input v-model="params.note" placeholder="note" style="width: 200px;" clearable />
        </el-form-item>
        <el-form-item label="developer">
          <el-input v-model="params.developer" placeholder="developer" style="width: 200px;" clearable />
        </el-form-item>
        <el-form-item label="producer">
          <el-input v-model="params.producer" placeholder="producer" style="width: 200px;" clearable />
        </el-form-item>
        <el-form-item label="tester">
          <el-input v-model="params.tester" placeholder="tester" style="width: 200px;" clearable />
        </el-form-item>
        <el-button @click="selectBotton">查询</el-button>
        <el-button @click="clearSearch">重置</el-button>
      </el-form>
    </div>
    <el-table :data="tableData">
      <!-- prop是tableData数组中，每个对象的具体key -->
      <el-table-column prop="appId" label="appId" />
      <el-table-column prop="note" label="APP名称" />
      <el-table-column prop="title" label="产品名称" />
      <el-table-column prop="developer" label="developer" />
      <el-table-column prop="producer" label="producer" />
      <el-table-column prop="tester" label="tester" />
      <el-table-column :formatter="formatDate" prop="updateDate" label="操作时间" />
      <el-table-column label="操作">
        <!-- slot-scope的意思是，el-table-column的组件中有相关的数据，在slot中给出了，在这里接住来使用，就是说可以用el-table-column子组件中slot的属性 可以是:XX='xx' 也可以直接xx='xx'，这个双引号中scope是任意的，取决于你在父组件中要用的变量名，会以key:value的形式存在scope这个对象中 -->
        <!-- 那么这里实际上就是el-table-column里有一个<slot :row=''>这样的标签，并把row的数据传了出来 -->
        <!-- <template slot-scope="scope">
          <el-link icon="el-icon-edit" @click="dialogProductUpdate(scope.row)">编辑</el-link>
          <el-link icon="el-icon-delete" @click="pDelete(scope.row)">删除</el-link>
        </template> -->
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
</template>

<script>
// 引用src/api/proudct 配置的请求列表方法
import { apiAppList, apiAppAdd } from '@/api/application'
import { apiProductListAll } from '@/api/product'
import store from '@/store'
import moment from 'moment'

export default {
  name: 'Application', // 页面名称
  // data() 数据\属性，固定return中配置
  data() {
    return {
      tableData: [],
      op_user: store.getters.name,
      application: {
        id: undefined,
        appId: undefined,
        productId: undefined,
        note: undefined,
        operator: this.op_user,
        tester: undefined,
        developer: undefined,
        producer: undefined,
        Ccmail: undefined,
        gitCode: undefined,
        wiki: undefined,
        more: undefined,
        createUser: this.op_user
      },
      drawerVisiable: false,
      appAction: 'ADD',
      options: [],
      params: {
        appId: '',
        productId: '',
        note: '',
        developer: '',
        producer: '',
        tester: '',
        page: 1,
        size: 10,
        total: 0
      },
      drawerRules: {
        appId: [
          { required: true, message: '请输应用名称', trigger: 'blur' }
        ],
        productId: [
          { required: true, message: '请选择所属范围', trigger: 'change' }
        ],
        tester: [
          { required: true, message: '测试人员是必填的', trigger: 'blur' }
        ],
        developer: [
          { required: true, message: '开发人员是必填的', trigger: 'blur' }
        ],
        producer: [
          { required: true, message: '产品是必填的', trigger: 'blur' }
        ],
        note: [
          { required: true, message: '名称是必填的', trigger: 'blur' }
        ]
      }
    }
  },
  // 页面生命周期中的创建阶段调用
  created() {
    // 调用methods的方法，即初次加载就请求数据
    this.getApplicationList()
    this.getProductList()
  },
  methods: {
    getApplicationList() {
      apiAppList(this.params).then(response => {
        this.tableData = response.data
        this.params.total = response.total
      })
    },

    getProductList() {
      apiProductListAll().then(res => {
        this.options = res.data
      })
    },

    selectBotton() {
      this.params.page = 1
      this.getApplicationList()
    },

    clearSearch() {
      this.params.appId = ''
      this.params.productId = ''
      this.params.note = ''
      this.params.developer = ''
      this.params.producer = ''
      this.params.tester = ''
    },

    formatDate(row, column) {
      const date = row[column.property]
      if (date === undefined) {
        return ''
      }
      return moment(date).utcOffset(0).format('YYYY-MM-DD HH:mm')
    },

    dialogApplication() {
      // 添加先初始化空状态
      this.application.id = undefined
      this.application.appId = ''
      this.application.productId = ''
      this.application.note = ''
      this.application.operator = this.op_user
      this.application.tester = ''
      this.application.developer = ''
      this.application.producer = ''
      this.application.Ccmail = ''
      this.application.gitCode = ''
      this.application.wiki = ''
      this.application.more = ''
      this.application.createUser = this.op_user

      // 弹出对话框设置为true
      this.drawerVisiable = true
    },
    commitApp(formdata) {
      this.$refs[formdata].validate((valid) => {
        if (valid) {
          apiAppAdd(this.application).then(() => {
            this.$notify({
              title: 'OK',
              message: '添加成功',
              type: 'success'
            })
            this.drawerVisiable = true
          })
        } else {
          return false
        }
      })
    },
    // pCreate() {
    //   // 请求API进行添加
    //   apiProductCreate(this.product).then(response => {
    //     // 如果request.js没有拦截即表示成功，给出对应提示和操作
    //     this.$notify({
    //       title: '成功',
    //       message: '项目或产品添加成功',
    //       type: 'success'
    //     })
    //     // 关闭对话框
    //     this.dialogAppShow = false
    //     // 重新查询刷新数据显示
    //     this.getProductList()
    //   })
    // },

    // dialogProductUpdate(row) {
    //   this.product.id = row.id
    //   this.product.keyCode = row.keyCode
    //   this.product.title = row.title
    //   this.product.desc = row.desc
    //   this.product.operator = this.op_user

    //   this.dialogAppStatus = 'UPDATE'
    //   this.dialogAppShow = true
    //   console.log(this.dialogAppStatus)
    // },

    // pUpdate() {
    //   apiProductUpdate(this.product).then(response => {
    //     this.$notify({
    //       title: '成功',
    //       message: '项目或产品修改成功',
    //       type: 'success'
    //     })
    //   }).catch(() => {
    //     this.$notify({
    //       title: '失败',
    //       message: '项目或产品修改失败',
    //       type: 'fail'
    //     })
    //   })
    //   this.dialogAppStatus = false
    //   this.getProductList()
    // },

    // pDelete(row) {
    //   this.$confirm('是否确认删除', '提示1', {
    //     confirmButtonText: '确认',
    //     cancelButtonText: '取消',
    //     type: 'warning'
    //   }).then(() => {
    //     this.product.id = row.id
    //     this.product.keyCode = row.keyCode
    //     this.product.title = row.title
    //     this.product.desc = row.desc
    //     this.product.operator = this.op_user
    //     apiProductDelete(this.product).then(response => {
    //       this.$notify({
    //         title: '成功',
    //         message: '项目删除成功',
    //         type: 'success'
    //       })
    //     })
    //     this.getProductList()
    //   }).catch(() => {
    //     this.$message({
    //       type: 'info',
    //       message: '取消删除'
    //     })
    //   })
    // },

    handleSizeChange(val) {
      this.params.size = val
      this.getApplicationList()
    },

    handleCurrentChange(val) {
      this.params.page = val
      this.getApplicationList()
    }
  }
}
</script>

<style scoped>
  .el-pagination {
      text-align: right;
  }
</style>
