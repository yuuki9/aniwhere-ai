"""샘플 문서: 실제 서비스에서는 DB/크롤링 데이터로 교체."""

DOCUMENTS: list[dict] = [
    {
        "id": "shop_hongdae_aniplus_01",
        "text": (
            "애니플러스 홍대점은 홍대입구역 인근에 있는 굿즈·가챠 전문 매장이다. "
            "최근 입고 안내에 주술회전 고죠 사토루 피규어 가챠(캡슐 머신) 라인이 "
            "전시되어 있었고, 교환·품절은 당일 재고에 따라 다르다."
        ),
        "metadata": {"area": "홍대", "has_gojo": "true", "type": "가챠샵"},
    },
    {
        "id": "shop_hongdae_randombox_02",
        "text": (
            "홍대 메인 상권의 랜덤박스·가챠 코너 매장. IP는 시즌마다 바뀌며 "
            "주술회전 캐릭터(고죠 포함) 랜덤 상품이 들어온 적이 있다. "
            "정확한 전시 위치는 매장 내 코너별로 나뉘어 있다."
        ),
        "metadata": {"area": "홍대", "has_gojo": "sometimes", "type": "가챠샵"},
    },
    {
        "id": "shop_gangnam_collect_03",
        "text": (
            "강남역 인근 콜렉터 샵. 주술회전 고죠 사토루 한정 굿즈가 종종 들어오지만 "
            "홍대가 아니라 강남 지역이다."
        ),
        "metadata": {"area": "강남", "has_gojo": "true", "type": "굿즈샵"},
    },
]
