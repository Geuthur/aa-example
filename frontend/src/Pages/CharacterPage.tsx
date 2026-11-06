// Third Party
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Alert, Card } from "react-bootstrap";
import { useTranslation } from "react-i18next";

// AA Example
import { characterQueryKeys, loadCharacters, updateCharacter } from "@/Api/calls/character";
import BaseSectionHeader from "@/Components/Base/BaseHeader";
import { CharacterTable } from "@/Components/Character/CharacterTable";

/** The character module page: lists the characters and queues updates. */
export const CharacterPage = () => {
  const { t } = useTranslation();
  const queryClient = useQueryClient();

  const { data, isLoading, isFetching, isError } = useQuery({
    queryKey: characterQueryKeys.all,
    queryFn: loadCharacters,
  });

  const updateMutation = useMutation({
    mutationFn: (characterId: number) => updateCharacter(characterId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: characterQueryKeys.all }),
  });

  return (
    <Card className="border-0 bg-transparent">
      <BaseSectionHeader name={t("Characters")} />
      {updateMutation.isSuccess && (
        <Alert variant="success" role="status">
          {updateMutation.data.message}
        </Alert>
      )}
      {updateMutation.isError && (
        <Alert variant="danger" role="alert">
          {t("The update could not be queued. Please try again.")}
        </Alert>
      )}
      <CharacterTable
        characters={data ?? []}
        isLoading={isLoading}
        isFetching={isFetching}
        isError={isError}
        onUpdate={(characterId) => updateMutation.mutate(characterId)}
        updatingCharacterId={updateMutation.isPending ? updateMutation.variables : undefined}
      />
    </Card>
  );
};

export default CharacterPage;
