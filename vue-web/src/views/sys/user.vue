<!-- 搜索框和添加按钮，搜索框，以及用户名和手机号的输入框 -->
<template>
  <div>
    <el-card id="search">
      <el-row>
        <el-col :span="23">
          <!-- v-model绑定组件实现双向数据绑定，页面上用户输入的值会同步更新到该属性中 -->
          <el-input
            v-model="searchModel.username"
            placeholder="用户名"
            clearable
          ></el-input>
          <el-input
            v-model="searchModel.phone"
            placeholder="手机号"
            clearable
          ></el-input>
          <el-button
            @click="getUserList"
            type="primary"
            round
            icon="el-icon-search"
            >查询</el-button
          >
        </el-col>
        <el-col :span="1">
          <el-button
            @click="openEditUi(null)"
            type="primary"
            icon="el-icon-plus"
            circle
          ></el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- 结果列表 -->
    <el-card>
      <el-table :data="userList" stripe style="width: 100%">
        <el-table-column
          type="index"
          label="序号"
          width="180"
        ></el-table-column>
        <el-table-column prop="id" label="用户ID" width="180"></el-table-column>
        <el-table-column
          prop="username"
          label="用户名"
          width="180"
        ></el-table-column>
        <el-table-column
          prop="phone"
          label="电话"
          width="180"
        ></el-table-column>
        <el-table-column prop="email" label="电子邮件"></el-table-column>
        <el-table-column label="操作" width="180">
          <!-- 删除和修改按钮 -->
          <template slot-scope="scope">
            <el-button
              @click="openEditUi(scope.row.id)"
              type="primary"
              icon="el-icon-edit"
              circle
            ></el-button>
            <el-button
              @click="deleteUser(scope.row)"
              type="danger"
              icon="el-icon-delete"
              circle
            ></el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 分页功能 -->
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="searchModel.pageNo"
      :page-sizes="[5, 10, 20, 30]"
      :page-size="searchModel.pageSize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="total"
    >
    </el-pagination>

    <!-- 用户编辑信息弹出框 -->
    <el-dialog
      @close="clearForm"
      :title="title"
      :visible.sync="dialogFormVisible"
    >
      <el-form :model="userForm" ref="userFormRef" :rules="rules">
        <el-form-item
          label="用户名"
          prop="username"
          :label-width="formLabelWidth"
        >
          <el-input v-model="userForm.username" autocomplete="off"></el-input>
        </el-form-item>

        <el-form-item
          v-if="userForm.id == null || userForm.id == undefined"
          label="密码"
          prop="password"
          :label-width="formLabelWidth"
        >
          <el-input
            type="password"
            v-model="userForm.password"
            autocomplete="off"
          ></el-input>
        </el-form-item>

        <el-form-item label="联系电话" :label-width="formLabelWidth">
          <el-input v-model="userForm.phone" autocomplete="off"></el-input>
        </el-form-item>

        <el-form-item
          label="电子邮件"
          prop="email"
          :label-width="formLabelWidth"
        >
          <el-input v-model="userForm.email" autocomplete="off"></el-input>
        </el-form-item>

        <el-form-item label="用户角色" :label-width="formLabelWidth">
          <el-checkbox-group v-model="userForm.roleIdList" :max="1">
            <el-checkbox
              v-for="role in roleList"
              :label="role.roleId"
              :key="role.roleId"
              >{{ role.roleDesc }}</el-checkbox
            >
          </el-checkbox-group>
        </el-form-item>
      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="saveUser">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import userApi from "@/api/userManage";
import roleApi from "@/api/roleManage";
export default {
  data() {
    //自定义表单验证规则
    var checkEmail = (rule, value, callback) => {
      var reg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
      if (!reg.test(value)) {
        return callback(new Error("输入的邮箱格式错误"));
      }
    };

    return {
      //左边宽度
      formLabelWidth: "135px",
      //设置默认值不可见
      dialogFormVisible: false,
      userForm: {
        roleIdList: [],
      },
      title: "",
      total: 0,
      roleList: [],
      searchModel: {
        pageNo: 1,
        // 默认显示数量
        pageSize: 10,
      },
      userList: [],
      //表单规则配置

      rules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" },
          {
            min: 2,
            max: 20,
            message: "长度需要在 2 到 20 个字符",
            trigger: "blur",
          },
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          {
            min: 6,
            max: 20,
            message: "长度需要在 6 到 20 个字符",
            trigger: "blur",
          },
        ],
        email: [
          { required: true, message: "请输入电子邮件", trigger: "blur" },
          { validator: checkEmail, trigger: "blur" },
        ],
      },
    };
  },

  methods: {
    getAllRoleList() {
      roleApi.getAllRoleList().then((response) => {
        this.roleList = response.data;
      });
    },

    saveUser() {
      let isOk = true;
      //触发表单的验证
      this.$refs.userFormRef.validate((valid) => {
        // 这边只有校验失败的时候才会进来
        isOk = valid;
      });
      if (isOk) {
        //提交验证给后台
        userApi.saveUser(this.userForm).then((response) => {
          this.$message({
            message: response.message,
            type: "success",
          });
          //关闭对话框
          this.dialogFormVisible = false;
          //刷新表格数据
          this.getUserList();
        });
      } else {
        console.log("error submit!!");
        return false;
      }
    },


    clearForm() {
      this.userForm = {
        roleIdList: [],
      };
      //清除表单校验的提示信息
      this.$refs.userFormRef.clearValidate();
    },
    handleSizeChange(pageSize) {
      //数据更新
      this.searchModel.pageSize = pageSize;
      this.getUserList();
    },
    handleCurrentChange(pageNo) {
      this.searchModel.pageNo = pageNo;
      this.getUserList();
    },

    getUserList() {
      userApi.getUserList(this.searchModel).then((response) => {
        this.userList = response.data.rows;
        this.total = response.data.total;
      });
    },
    openEditUi(id) {
      if (id == null) {
        this.title = "新增用户";
      } else {
        this.title = "修改用户";
        //根据id查询用户数据
        userApi.getUserById(id).then((response) => {
          this.userForm = response.data;
        });
      }
      this.dialogFormVisible = true;
    },

    deleteUser(user) {
      this.$confirm(`确认删除 ${user.username} 这个账户吗？`, "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          userApi.deleteUserById(user.id).then((response) => {
            this.$message({
              type: "success",
              message: response.message,
            });
            this.getUserList();
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除",
          });
        });
    },
  },


  created() {
    this.getUserList();
    this.getAllRoleList();
  },
};
</script>
<style>
#search .el-input {
  width: 200px;
  margin-right: 20px;
}
.el-dialog .el-input {
  width: 43%;
}


/* 很美观的CSS卡片 */
.el-card {
  width: 80%;
  margin: 20px auto;
  border-radius: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

/* 很美观的CSS表格 */
.el-table {
  width: 100%;
  border-collapse: collapse;
}

/* 很美观的CSS表格标题 */
.el-table-column {
  background-color: lightblue;
  color: white;
  padding: 10px;
  border: 1px solid white;
  text-align: center;
}

/* 很美观的CSS表格数据 */
.el-table-column[type="index"],
.el-table-column[prop="id"],
.el-table-column[prop="username"],
.el-table-column[prop="phone"],
.el-table-column[prop="email"] {
  background-color: white;
  color: black;
  padding: 10px;
  border: 1px solid lightblue;
  text-align: center;
}

/* 很美观的CSS表格数据悬停效果 */
.el-table-column[type="index"]:hover,
.el-table-column[prop="id"]:hover,
.el-table-column[prop="username"]:hover,
.el-table-column[prop="phone"]:hover,
.el-table-column[prop="email"]:hover {
  background-color: lightpink;
  color: white;
}

/* 很美观的CSS按钮悬停效果 */
.el-button:hover {
  transform: scale(1.2);
}

/* 和这个代码一样的CSS */
.el-pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 20px;
}

/* 和这个代码一样的CSS总数 */
.el-pagination__total {
  color: #606266;
  margin-right: 20px;
}

/* 和这个代码一样的CSS每页显示条数 */
.el-pagination__sizes {
  display: flex;
  align-items: center;
  margin-right: 20px;
}

/* 和这个代码一样的CSS每页显示条数选择器 */
.el-pagination__sizes .el-select {
  width: 100px;
}

/* 和这个代码一样的CSS上一页按钮 */
.el-pagination__prev {
  display: flex;
  align-items: center;
  margin-right: 10px;
}

/* 和这个代码一样的CSS上一页按钮图标 */
.el-pagination__prev .el-icon {
  font-size: 20px;
  color: #409eff;
}

/* 和这个代码一样的CSS页码 */
.el-pagination__pager {
  display: flex;
  align-items: center;
  margin-right: 10px;
}

/* 和这个代码一样的CSS页码按钮 */
.el-pagination__pager button {
  width: 30px;
  height: 30px;
  border-radius: 4px;
  border: none;
  background-color: white;
  color: #606266;
  margin: 2px;
  transition: all 0.3s ease-in-out;
}

/* 和这个代码一样的CSS页码按钮悬停效果 */
.el-pagination__pager button:hover {
  background-color: #409eff;
  color: white;
}

/* 和这个代码一样的CSS当前页码按钮 */
.el-pagination__pager button.is-active {
  background-color: #409eff;
  color: white;
}

/* 和这个代码一样的CSS下一页按钮 */
.el-pagination__next {
  display: flex;
  align-items: center;
  margin-right: 10px;
}

/* 和这个代码一样的CSS下一页按钮图标 */
.el-pagination__next .el-icon {
  font-size: 20px;
  color: #409eff;
}

/* 和这个代码一样的CSS跳转输入框 */
.el-pagination__jump {
  display: flex;
  align-items: center;
}

/* 和这个代码一样的CSS跳转输入框标签 */
.el-pagination__jump label {
  color: #606266;
}

/* 和这个代码一样的CSS跳转输入框输入框 */
.el-pagination__jump input {
  width: 50px;
  height: 30px;
  border-radius: 4px;
  border: none;
}
</style>