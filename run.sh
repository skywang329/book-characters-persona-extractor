FILEPATHS=()

for filePath in "/shared/0/projects/contextual-offensiveness/data/bookfiles/"*
do
	FILEPATHS+=("$filePath")
done

SUB='.txt'
echo "done."

for filePath in "${FILEPATHS[@]}"
do
	if [[ "$filePath" == *"$SUB"* ]]; then
		filePathBasename=`basename "$filePath" .txt`
		awk '{printf "novels/BookNLP -doc %s -p %s -tok %s -f -d", $filePath, $filePathToSave, $filePathToSaveTokens}'
	fi
done | xargs -0 -x -n 1 -P 2 ./runjava