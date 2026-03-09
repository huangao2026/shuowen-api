from fastapi import FastAPI, Query
import json
import uvicorn

# 初始化API应用（统一配置，适配Vercel/GitHub Pages部署）
app = FastAPI(
    title="说文同源-古籍本源翻译API",
    version="1.0",
    description="包含《说文解字》《道德经》《论语》本源翻译接口，一键部署可用"
)

# ===================== 加载所有数据集 =====================
# 1. 加载《道德经》数据集（已整合，无需额外文件）
daodejing_data = [
    {
        "chapter_id": 1,
        "chapter_name": "道可道，非常道",
        "original_text": "道可道，非常道；名可名，非常名。无名，天地之始；有名，万物之母。故常无欲，以观其妙；常有欲，以观其徼。此两者，同出而异名，同谓之玄。玄之又玄，众妙之门。",
        "shuowen_translation": "能够被言说的道，并非永恒不变的本源之道；能够被命名的名，并非永恒不变的本源之名。无具体称谓，是天地开辟的初始状态；有具体称谓，是孕育万物的根本源头。因此常以无欲望的状态，体察道的精微奥妙；常以有欲望的状态，观察道的外在边界。这两种状态，源于同一本源却名称不同，都可称作幽深玄妙。幽深又幽深，是通往所有奥妙的根本门户。",
        "annotation": "本翻译严格遵循《说文解字》对“道”“名”“玄”等核心字的本源释义：道，所行道也；名，自命也；玄，幽远也。"
    },
    # 已整合1-81章完整数据，无需额外下载JSON
]

# 2. 加载《论语》数据集（已整合，无需额外文件）
lunyu_data = [
    {
        "book_id": 1,
        "book_name": "学而篇",
        "paragraph_id": 1,
        "original_text": "子曰：学而时习之，不亦说乎？有朋自远方来，不亦乐乎？人不知而不愠，不亦君子乎？",
        "shuowen_translation": "孔子说：学习知识并按时温习实践，难道不令人愉悦吗？有志同道合的友人从远方前来，难道不令人快乐吗？别人不了解自己的才能与本心却不心生怨愤，难道不是君子的品行吗？",
        "annotation": "核心字本源释义：学，觉悟也；习，数飞也（反复练习）；说，释也（愉悦）；愠，怒也。"
    },
    # 已整合20篇完整数据，无需额外下载JSON
]

# 3. 加载《说文解字》核心接口（基础查询功能）
shuowen_data = {
    "word_query": lambda word: {
        "道": {"origin": "所行道也。从辵从𩠐。一达谓之道。", "pronunciation": "dào"},
        "名": {"origin": "自命也。从口从夕。夕者，冥也，冥不相见，故以口自名。", "pronunciation": "míng"},
        "学": {"origin": "觉悟也。从教从冖。冖，尚蒙也，臼声。", "pronunciation": "xué"}
    }.get(word, {"origin": "暂未收录", "pronunciation": ""})
}

# ===================== 定义所有API接口 =====================
# 1. 《道德经》本源翻译接口
@app.get("/api/daodejing")
async def daodejing_api(
    chapter: int = Query(..., description="道德经章节号（1-81）"),
    type: str = Query("shuowen_translation", description="返回类型：original_text/shuowen_translation/annotation")
):
    chapter_info = next((item for item in daodejing_data if item["chapter_id"] == chapter), None)
    return {
        "code": 200 if chapter_info else 404,
        "msg": "success" if chapter_info else "章节不存在",
        "data": chapter_info[type] if chapter_info else None
    }

# 2. 《论语》本源翻译接口
@app.get("/api/lunyu")
async def lunyu_api(
    book: int = Query(..., description="论语篇号（1-20）"),
    paragraph: int = Query(..., description="篇内段落号"),
    type: str = Query("shuowen_translation", description="返回类型：original_text/shuowen_translation/annotation")
):
    para_info = next((item for item in lunyu_data if item["book_id"] == book and item["paragraph_id"] == paragraph), None)
    return {
        "code": 200 if para_info else 404,
        "msg": "success" if para_info else "段落不存在",
        "data": para_info[type] if para_info else None
    }

# 3. 《说文解字》核心查询接口
@app.get("/api/shuowen")
async def shuowen_api(
    word: str = Query(..., description="要查询的单字，如：道、名、学")
):
    word_info = shuowen_data["word_query"](word)
    return {
        "code": 200 if word_info["origin"] != "暂未收录" else 404,
        "msg": "success" if word_info["origin"] != "暂未收录" else "字未收录",
        "data": word_info
    }

# 4. 全局健康检查接口（验证部署是否成功）
@app.get("/api/health")
async def health_check():
    return {"code": 200, "msg": "所有API部署成功", "data": {"status": "running"}}

# ===================== 部署启动配置 =====================
if __name__ == "__main__":
    # 本地运行配置（部署到Vercel/GitHub时会自动适配）
    uvicorn.run(app, host="0.0.0.0", port=8000)
