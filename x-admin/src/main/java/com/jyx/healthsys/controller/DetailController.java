package com.jyx.healthsys.controller;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.jyx.Data_unification.Unification;
import com.jyx.healthsys.entity.Detail;
import com.jyx.healthsys.service.IDetailService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Tag(name = "病情运动详情", description = "病情与运动关联的CRUD及查询接口")
@RestController
@RequestMapping("/detail")
public class DetailController {


    @Autowired
    private IDetailService detailService;


    @Operation(summary = "根据运动名称查询病情关联详情")
    @GetMapping("/DetailInfo/{sportName}")
    public Unification<Detail> getDetailInfo(
            @Parameter(description = "运动名称") @PathVariable String sportName) {
        List<Detail> detailList = detailService.getDetailInfo(sportName);

        System.out.println(detailList);
        if (detailList == null || detailList.isEmpty()) {
            return Unification.fail("查询结果为空");
        }
        Detail detail = detailList.get(0);
        return Unification.success(detail);
    }


    @Operation(summary = "分页获取病情运动详情列表")
    @GetMapping("/getDetailList")
    public Unification<Map<String,Object>> getDetailList(
            @Parameter(description = "运动类型（可选筛选）") @RequestParam(value = "sportType", required = false) String sportType,
            @Parameter(description = "当前页码") @RequestParam("pageNo") Long pageNo,
            @Parameter(description = "每页条数") @RequestParam("pageSize") Long pageSize) {

        LambdaQueryWrapper<Detail> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(StringUtils.hasLength(sportType), Detail::getSportType, sportType);
        Page<Detail> page = new Page<>(pageNo, pageSize);

        detailService.page(page, wrapper);
        Map<String, Object> data = new HashMap<>();

        data.put("total", page.getTotal());
        data.put("rows", page.getRecords());
        System.out.println(data);
        return Unification.success(data);
    }


    @Operation(summary = "新增病情运动详情")
    @PostMapping("/addDetail")
    public Unification<?> addDetail(@RequestBody Detail detail) {
        boolean isSuccess = detailService.addDetail(detail);
        if (isSuccess) {
            return Unification.success("新增成功");
        } else {
            return Unification.fail("新增失败，运动类型已存在");
        }
    }


    @Operation(summary = "修改病情运动详情")
    @PutMapping("/updateDetail")
    public Unification<?> updateDetail(@RequestBody Detail detail){
        detailService.updateDetail(detail);
        return Unification.success("修改成功");
    }


    @Operation(summary = "根据ID获取病情运动详情")
    @GetMapping("/getDetailById/{id}")
    public Unification<Detail> getDetailById(
            @Parameter(description = "详情ID") @PathVariable("id") Integer id){
        Detail detail = detailService.getDetailById(id);
        return  Unification.success(detail);
    }


    @Operation(summary = "根据ID删除病情运动详情")
    @DeleteMapping("/deleteDetailById/{id}")
    public Unification<Detail> deleteDetailById(
            @Parameter(description = "详情ID") @PathVariable("id") Integer id){
        detailService.deletDetailById(id);
        return  Unification.success("删除成功");
    }


}
