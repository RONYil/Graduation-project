def remove_lines_with_tags(input_file, output_file, tags_to_remove):
    try:
        # 打开原始文本文件进行读取
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 删除包含指定标签的整行
        modified_lines = [line for line in lines if not any(tag in line for tag in tags_to_remove)]

        # 打开目标文本文件进行写入
        with open(output_file, 'w', encoding='utf-8') as file:
            file.writelines(modified_lines)

        print("包含指定标签的整行已成功删除并保存到文件：", output_file)

    except FileNotFoundError:
        print("文件未找到")
    except Exception as e:
        print("发生错误：", str(e))




input_file = 'all_raw_data.txt'  # 替换为你的输入文件名
output_file = 'Data_deletion_output.txt'  # 替换为你的输出文件名
tags_to_remove = ['企业名称', '企业地址', '药物过量', '老年患者用药', '儿童用药', '妊娠期妇女及哺乳期妇女用药', '药代动力学', '药理毒理', '药物相互作用', '执行标准', '贮藏', '包装', '有效期', '批准文号', '生产厂家', '生产企业', '药理作用', '保质期', '规格', '不良反应', '注意事项', '作用类别', '警告']  # 替换为你想删除的标签列表

remove_lines_with_tags(input_file, output_file, tags_to_remove)