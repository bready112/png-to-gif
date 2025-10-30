from PIL import Image
import os

def pngs_to_gif(png_folder, output_path, duration=500):
    """PNG 파일들을 GIF 애니메이션으로 변환"""
    # PNG 파일 목록 정렬 (대소문자 무시)
    png_files = sorted([f for f in os.listdir(png_folder) if f.lower().endswith('.png')])
    if not png_files:
        raise FileNotFoundError(f"No PNG files found in {png_folder}")

    # 첫 이미지로 크기 결정
    first = Image.open(os.path.join(png_folder, png_files[0]))
    frames = []
    
    # 모든 이미지를 같은 크기로 변환하여 프레임 추가
    for png in png_files:
        img = Image.open(os.path.join(png_folder, png))
        if img.size != first.size:
            img = img.resize(first.size)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        frames.append(img)

    # GIF 저장
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
        optimize=False
    )
    return output_path

if __name__ == "__main__":
    import argparse
    import sys

    # 실행 파일/스크립트 위치 확인
    if getattr(sys, "frozen", False):
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # GIF 폴더는 한 번만 생성
    gif_dir = os.path.join(script_dir, "GIF")
    os.makedirs(gif_dir, exist_ok=True)

    parser = argparse.ArgumentParser(description="폴더 내 PNG들을 GIF로 변환합니다.")
    parser.add_argument("-i", "--input", required=False, default=script_dir,
                    help=f"PNG 파일들이 있는 폴더 (기본: {script_dir})")
    parser.add_argument("-o", "--output", required=False, default="output.gif",
                    help="출력 GIF 파일명 (기본: output.gif)")
    parser.add_argument("-d", "--duration", type=int, default=42,
                    help="각 프레임 지속 시간(ms) (기본: 42)")
    args = parser.parse_args()

    # 출력 파일 설정
    out_name = os.path.basename(args.output)
    if not out_name.lower().endswith('.gif'):
        out_name += '.gif'
    output_path = os.path.join(gif_dir, out_name)

    # GIF 생성
    out = pngs_to_gif(args.input, output_path, args.duration)
    print(f"완료. GIF 저장: {out}")