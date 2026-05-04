<template>
  <div>
    <div class="search-wrapper">
      <el-row class="search-row">
        <el-col :span="8" :offset="8">
          <el-button
            class="search-button"
            icon="el-icon-search"
            @click="showSearchBox"
            >点击这里进行搜索</el-button
          >
        </el-col>
      </el-row>
      <el-dialog title="搜索健康知识" :visible.sync="showDialog">
        <el-input
          placeholder="请输入你想要的内容"
          v-model="searchText"
        ></el-input>
        <el-button slot="footer" @click="closeDialog">取消</el-button>
        <el-button slot="footer" type="primary" @click="Search">搜索</el-button>
      </el-dialog>
    </div>

    

    <div class="grid-container">
      <div class="grid-item" v-for="(sportInfo, index) in sportInfos" :key="index">
        <h2>{{ sportInfo.sportType }}</h2>
        <p>运动种类：{{ sportInfo.sportType }}</p>
        <p>适宜时间：{{ sportInfo.suitableTime }}</p>
        <p>适宜心率：{{ sportInfo.suitableHeartRate }}</p>
        <p>适宜频率：{{ sportInfo.suitableFrequency }}</p>
        <p>推荐速度：{{ sportInfo.recommendedSpeed }}</p>
        <button @click="goToDetail(sportInfo.sportType, sportInfo)">
          查看详情
        </button>
      </div>
    </div>


  </div>
</template>

<script>
import sportApi from "@/api/Function_Menu";

export default {
  data() {
    return {
      showDialog: false,
      searchText: "",
      sportInfos: [],
      DetailInfo: [],
    };
  },

  async created() {
    await this.showSearch();
  },

  methods: {
    goToDetail(sportName, sportInfo) {
      sportApi
        .DetailInfo(sportName)
        .then((response) => {
          const detailInfo = response.data;
          // 将this.DetailInfo与sportInfo合并
          const mergedInfo = { ...detailInfo, ...sportInfo };
          console.log(detailInfo);
          // 传递参数并跳转
          this.$router.push({ path: "/detail", query: mergedInfo });
        })
        .catch((error) => {
          console.error(error);
        });
    },

    closeDialog() {
      this.showDialog = false;
    },

    showSearchBox() {
      this.searchText = ""; // 重置搜索框
      this.showDialog = true;
    },

    async showSearch() {
      try {
        const response = await sportApi.getAllSportInfo();
        // 取得运动信息数组
        const sportInfoData = response.data.sportInfos;
        const sportInfos = sportInfoData.slice();
        // 重构每条运动信息的数据格式
        this.sportInfos = sportInfos.map((info) => ({
          id: info.id,
          sportType: info.sportType,
          suitableTime: info.suitableTime,
          suitableHeartRate: info.suitableHeartRate,
          suitableFrequency: info.suitableFrequency,
          recommendedSpeed: info.recommendedSpeed,
        }));
        this.$message({
          message: "查询成功",
          type: "success",
        });
      } catch (error) {
        console.log(error);
      }
    },

      async Search() {
        try {
          const response = await sportApi.getAllSportInfo();
          const sportInfoData = response.data.sportInfos;
          // 根据输入的搜索内容进行过滤
          const filteredSportInfoData = sportInfoData.filter((info) => {
            return info.sportType.includes(this.searchText);
          });
          // 重构每条运动信息的数据格式
          const sportInfos = filteredSportInfoData.map((info) => ({
            id: info.id,
            sportType: info.sportType,
            suitableTime: info.suitableTime,
            suitableHeartRate: info.suitableHeartRate,
            suitableFrequency: info.suitableFrequency,
            recommendedSpeed: info.recommendedSpeed,
          }));
          // 更新运动信息列表
          this.sportInfos = sportInfos;
          // 隐藏搜索框
          this.showDialog = false;
          this.$message({
            message: "查询成功",
            type: "success",
          });
        } catch (error) {
          console.log(error);
        }
      },
  },
};
</script>



<style >
button {
  padding: 1rem 2rem;
  background-color: #4caf50;
  border: none;
  border-radius: 0.5rem;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

button:hover {
  background-color: #3e8e41;
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-gap: 20px;
  margin: 20px;
}

.grid-item {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  background-color: #fff;
  border: 1px solid #ccc;
  padding: 20px;
  cursor: pointer;
  border-radius: 10px;
}

.grid-item:hover {
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.grid-item h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: bold;
  text-align: center;
  color: #333;
}

.grid-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}

.grid-label {
  font-size: 0.8rem;
  font-weight: bold;
  color: #666;
}

.grid-value {
  font-size: 1.2rem;
  font-weight: bold;
  color: #333;
}

.grid-button {
  margin-top: 20px;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: #007bff;
  color: #fff;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.grid-button:hover {
  background-color: #0062cc;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.search-wrapper {
  padding-top: 20px;
}

.search-row {
  text-align: center;
}

.search-button {
}
</style>