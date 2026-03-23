import csv
import pickle   # 이진 파일 저장/읽기를 위해 사용

try:
    # 1. CSV 읽기
    with open('Mars_Base_Inventory_List.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    # 2. 출력
    print('전체 데이터:')
    for row in data:
        print(row)

    # 3. 인화성 기준 정렬 (내림차순)
    sorted_data = sorted(data, key=lambda x: float(x['Flammability']), reverse=True)

    print('\n인화성 높은 순 정렬:')
    for row in sorted_data:
        print(row)

    # 4. 인화성 지수 0.7 이상 필터링
    dangerous_items = [row for row in sorted_data if float(row['Flammability']) >= 0.7]

    print('\n인화성 지수 0.7 이상:')
    for row in dangerous_items:
        print(row)

    # 5. 새로운 CSV 저장
    with open('Mars_Base_Inventory_danger.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(dangerous_items)

    print('\nMars_Base_Inventory_danger.csv 파일 저장 완료!')

    # === 보너스 과제 추가 ===
    # 6. 인화성 순서로 정렬된 배열을 이진 파일로 저장
    with open('Mars_Base_Inventory_List.bin', 'wb') as f:
        pickle.dump(sorted_data, f)

    print('\nMars_Base_Inventory_List.bin 파일 저장 완료!')

    # 7. 저장된 이진 파일 다시 읽어서 출력
    with open('Mars_Base_Inventory_List.bin', 'rb') as f:
        loaded_data = pickle.load(f)

    print('\nMars_Base_Inventory_List.bin 파일에서 읽은 데이터:')
    for row in loaded_data:
        print(row)

    # 8. 예외 처리
except FileNotFoundError:
    print('CSV 파일을 찾을 수 없습니다. 파일 이름과 경로를 확인하세요.')
except Exception as e:
    print('오류 발생:', e)