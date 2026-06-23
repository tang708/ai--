package com.jyx.healthsys.controller;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.conditions.query.ChainQuery;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.jyx.Data_unification.Unification;
import com.jyx.healthsys.entity.*;
import com.jyx.healthsys.service.IDetailService;
import com.jyx.healthsys.service.ISportInfoService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Tag(name = "运动知识管理", description = "运动知识CRUD及查询接口")
@RestController
@RequestMapping("/sport")
public class SportInfoController {

    @Autowired
    private ISportInfoService sportInfoService;


    @Operation(summary = "获取全部运动知识")
    @GetMapping("/getAllSportInfo")
    public Map<String, Object> getAllSportInfo() {
        List<SportInfo> sportInfos = sportInfoService.getAllSportInfos();
        Map<String, Object> response = new HashMap<>();
        Map<String, Object> data = new HashMap<>();
        data.put("sportInfos", sportInfos);
        response.put("code", 20000);
        response.put("message", "success");
        response.put("data", data);
        return response;
    }


    @Operation(summary = "分页获取运动知识列表")
    @GetMapping("/getSportList")
    public Unification<Map<String,Object>> getSportList(
            @Parameter(description = "运动类型（可选筛选）") @RequestParam(value = "sportType", required = false) String sportType,
            @Parameter(description = "当前页码") @RequestParam("pageNo") Long pageNo,
            @Parameter(description = "每页条数") @RequestParam("pageSize") Long pageSize) {

        LambdaQueryWrapper<SportInfo> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(StringUtils.hasLength(sportType), SportInfo::getSportType, sportType);
        Page<SportInfo> page = new Page<>(pageNo, pageSize);

        sportInfoService.page(page, wrapper);
        Map<String, Object> data = new HashMap<>();

        data.put("total", page.getTotal());
        data.put("rows", page.getRecords());
        return Unification.success(data);
    }


    @Operation(summary = "新增运动知识")
    @PostMapping("/add")
    public Unification<?> addSport(@RequestBody SportInfo sport) {
        boolean isSuccess = sportInfoService.addSport(sport);
        if (isSuccess) {
            return Unification.success("新增成功");
        } else {
            return Unification.fail("新增失败，运动类型已存在");
        }
    }


    @Operation(summary = "修改运动知识")
    @PutMapping("/update")
    public Unification<?> updateSport(@RequestBody SportInfo sport){
        sportInfoService.updateSport(sport);
        return Unification.success("修改成功");
    }


    @Operation(summary = "根据ID获取运动知识详情")
    @GetMapping("/{id}")
    public Unification<SportInfo> getSportById(
            @Parameter(description = "运动知识ID") @PathVariable("id") Integer id){
        SportInfo sportInfo = sportInfoService.getSportById(id);
        return  Unification.success(sportInfo);
    }


    @Operation(summary = "根据ID删除运动知识")
    @DeleteMapping("/{id}")
    public Unification<SportInfo> deletSportById(
            @Parameter(description = "运动知识ID") @PathVariable("id") Integer id){
        sportInfoService.deletUserById(id);
        return  Unification.success("删除成功");
    }


}
